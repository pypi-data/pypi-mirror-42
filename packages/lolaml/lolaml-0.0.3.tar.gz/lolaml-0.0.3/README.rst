``LolaML`` - track your ML experiments
======================================

.. image:: https://readthedocs.org/projects/lolaml/badge/?version=latest
   :target: https://lolaml.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://gitlab.com/stefan-otte/lolaml/badges/master/pipeline.svg
   :target: https://gitlab.com/stefan-otte/lolaml/commits/master
   :alt: Pipeline Status

.. image:: https://gitlab.com/stefan-otte/lolaml/badges/master/coverage.svg
   :target: https://gitlab.com/stefan-otte/lolaml/commits/master
   :alt: Coverage Report

.. image:: https://img.shields.io/pypi/v/lolaml.svg
   :target: https://pypi.org/project/lolaml
   :alt: PyPI Version

.. [![Windows Build Status](https://img.shields.io/appveyor/ci/sotte/lolaml/master.svg?label=window)](https://ci.appveyor.com/project/sotte/lolaml)
.. [![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/sotte/lolaml.svg)](https://scrutinizer-ci.com/g/sotte/lolaml/?branch=master)

Track your machine learning experiments with LolaML,
never lose any information or forget which parameter yielded which results.
Lola creates a simple JSON representation of the run that contains all the
information you logged.
The JSON can easily be shared to collaborate with friends and colleagues.
Lola strives to be non-magic and simple but configurable.

**Features:**

- a simple logging interface
- a simple representation of the logged data
- works with any machine learning library
- automatically creates an artifact folder for each run
- automatically uploads artifacts to a remote bucket (if you want)
- simple jupyter notebook dashboard (more to come...)

::

    import lolaml as lola

    # Use the run context manager to start/end a run
    with lola.Run(project="mnist", prefix_path="data/experiments") as run:
        # a unique id for the run
        print(run.run_id)
        # store all artifacts (model files, images, etc.) here
        print(run.path)  # -> data/experiments/<run_id>

        run.log_param("lr", 0.1)
        run.log_param("epochs", 10)

        run.log_tags("WIP", "RNN")

        # Create and train your model...

        run.log_metric("loss", loss, step=1)
        run.log_metric("train_acc", train_acc, step=1)
        run.log_metric("val_acc", val_acc, step=1)

        model.save(os.path.join(run.path, "model.pkl"))

    # After a run there is a lola_run*.json file under run.path.
    # It contails all the information you logged.

After the run there is a JSON file that looks something like this::

    {
        "project": "mnist",
        "run_id": "9a531da0-dc43-4dcc-8968-77fd480ff7ee",
        "status": "done",
        "path": "data/experiments/9a531da0-dc43-4dcc-8968-77fd480ff7ee",
        "user": "stefan",
        "start_time": "2019-02-16 12:49:32.782958",
        "end_time": "2019-02-16 12:49:32.814529",
        "metrics": [
            {
                "name": "loss",
                "value": 1.5
                "step": 1,
                "ts": "2019-02-16 12:49:32.813750"
            },
            ...
        ],
        "params": {
            "lr": "0.1",
            "epochs": 10,
        },
        "tags": ["WIP", "RNN"],
        "artifacts": {
            "data/experiments/9a531da0-dc43-4dcc-8968-77fd480ff7ee/lola_run_9a531da0-dc43-4dcc-8968-77fd480ff7ee.json": {},
            ...
        },
        "git": {
            "sha": "41cb4fb11b7e937c602c2282b9275200c88b8797",
            "status": "...",
            "diff": "...",
        },
        "call_info": {
            "__file__": "somefile.py",
            "argv": [],
        }
    }


Lola can automatically upload all artifacts to a remote storage bucket for you::

  with lola.run(
      remote_location="gs://somewhere",
      remote_credentials="service_account.json",
  ) as run:
      # train and log ...

  # All artifacts are uploaded now


The remote location can also be configured with the `.lola.toml` file.

Additionally, Lola offers some helpers to analyse the your experiments:

TODO add image of dashboard

Setup
=====

Requirements
------------

* Python 3.6+

Installation
------------

Install this library directly into an activated virtual environment::

    $ pip install lolaml

or add it to your `Poetry <https://poetry.eustace.io/>`_ project::

    $ poetry add lolaml

Misc
====

This project was generated with `cookiecutter <https://github.com/audreyr/cookiecutter>`_
using `jacebrowning/template-python <https://github.com/jacebrowning/template-python>`_.
Thanks!
