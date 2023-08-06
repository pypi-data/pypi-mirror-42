"""
HERE BE DRAGONS.

Everything in incubator.py is subject to breaking changes.
Use at your own risk.

"""
import json
from pathlib import Path
from typing import Callable, Tuple, Union

import altair as alt
import log
import pandas as pd


def read_json_runs(glob_pattern: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Glob for the pattern and read the json runs."""
    lola_jsons = sorted(list(Path().glob(glob_pattern)))
    log.info(f"# Loading {len(lola_jsons)} lola runs...")
    if len(lola_jsons) == 0:
        return None, None
    lola_runs = [json.load(file.open()) for file in lola_jsons]

    # df_metrics is a table of metrics
    df_metrics = pd.io.json.json_normalize(
        lola_runs, record_path="metrics", meta="run_id"
    )[["run_id", "name", "value", "step", "ts"]]

    # df_overview will contain one row for each run with all relevant overview information
    df_overview = pd.io.json.json_normalize(lola_runs)
    col_order = [
        "project",
        "run_id",
        "status",
        "path",
        "user",
        "start_time",
        "end_time",
        # "git_sha",
        # "git_diff",
        # "git_status",
        *sorted(
            [col for col in df_overview.columns.tolist() if col.startswith("params.")]
        ),
    ]
    df_overview = df_overview[col_order]

    def _aggregate_metrics(
        df_metrics: pd.DataFrame,
        agg_fn: Union[Callable, str] = "max",
        agg_name: str = "max",
    ) -> pd.DataFrame:
        """Aggregate and reshape."""
        # get the min values per group, ...
        df_agg = (
            df_metrics.groupby(["run_id", "name"])
            .agg({"value": agg_fn})
            .reset_index()
            .pivot_table(values="value", index="run_id", columns="name")
            .reset_index()
        )
        columns = df_agg.columns.to_list()
        df_agg = df_agg.rename(
            columns={
                col: f"metric.{col}.{agg_name}" for col in columns if col != "run_id"
            }
        )
        return df_agg

    metrics_max = _aggregate_metrics(df_metrics, agg_fn="max", agg_name="max")
    df_overview = df_overview.merge(metrics_max, on="run_id")

    metrics_min = _aggregate_metrics(df_metrics, agg_fn="min", agg_name="min")
    df_overview = df_overview.merge(metrics_min, on="run_id")

    return df_overview, df_metrics


def _esc(name: str) -> str:
    r"""
    Escape altair field names that contain a dot.

    Dots, i.e. ".", in field names are interpreted as hierachical access,
    but quite often they are not.

    Examples:
        >>> _esc("foo.bar") == "foo\\.bar"
        True
        >>> _esc("foo_bar") == "foo_bar"
        True

    """
    return name.replace(".", "\\.")


def plot_overview(df_overview: pd.DataFrame) -> alt.Chart:
    plot_max = (
        alt.Chart(df_overview)
        .mark_bar()
        .encode(x=alt.X("run_id:N"), y=alt.Y(_esc("metric.val_loss.max:Q")))
    )
    plot_min = (
        alt.Chart(df_overview)
        .mark_bar()
        .encode(x=alt.X("run_id:N"), y=alt.Y(_esc("metric.val_loss.min:Q")))
    )
    return plot_min | plot_max


def plot_metrics_siple(df_metrics: pd.DataFrame) -> alt.Chart:
    plot = (
        alt.Chart(df_metrics)
        .mark_line()
        .encode(x="step:Q", y="value:Q", column="name", color=alt.Color("run_id:N"))
        .interactive()
    )
    return plot
