import json
from dataclasses import asdict
from pathlib import Path

import log

from lolaml.data import RunData


class Storage:
    @staticmethod
    def write(data: RunData) -> None:
        raise NotADirectoryError()

    @staticmethod
    def read(path: str) -> RunData:
        raise NotADirectoryError()


class JSONStorage(Storage):
    """JSONStorage stores a json representation of the `RunData`."""

    @staticmethod
    def write(data: RunData) -> None:
        dst = data.run_file
        Path(dst).parent.mkdir(parents=True, exist_ok=True)
        log.info(f"# Storing run under '{dst}'")

        with open(dst, "w") as f:
            f.write(json.dumps(asdict(data)))

    @staticmethod
    def read(path: str) -> RunData:
        with open(path, "r") as f:
            return RunData(**json.loads(f.read()))
