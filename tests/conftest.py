# pylint: disable=import-outside-toplevel
"""conftest.py - custom pytest-plugins.

This file contains the configurations that we need for running our tests:
For more information about conftest.py, please see:

 - https://docs.pytest.org/en/latest/writing_plugins.html
 - https://pytest-flask.readthedocs.io/en/latest/tutorial.html
 - https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files

The "_helpers"-directory contains code that can be re-used in various tests.

Note: The tests-directory itself is NOT a python-package (no __init__.py).
Please avoid putting an __init.py-file in this directory.

If you by accident put an __init__.py in this tests-directory,
you will not be able to run pytest, instead it will fail with:

    > ImportError: Error importing plugin "_helpers": No module named '_helpers'

"""

import typing as tp

import pytest
from airflow.models import DagBag
from airflow.sdk import DAG


@pytest.fixture
def sample_data() -> dict:
    """Provide sample data for tests."""
    return {"key": "value", "count": 42}


@pytest.fixture
def sample_list() -> list[str]:
    """Provide a sample list for tests."""
    return ["foo", "bar", "baz"]


def get_dag(dag_bag: DagBag, dag_id: str) -> DAG:
    """Get a DAG from the bag and assert it exists."""
    dag = dag_bag.get_dag(dag_id)
    assert dag is not None
    return dag


def get_result(results: tp.Any, task_id: str) -> tp.Any:  # noqa: ANN401
    """Return the result of a task execution."""
    ti = results.get_task_instance(task_id=task_id)
    return ti.xcom_pull(task_ids=task_id, key="return_value")


@pytest.fixture(scope="session")
def dag_bag() -> DagBag:
    """Load all DAGs from the configured dags folder."""
    from airflow.configuration import conf

    dags_folder = conf.get("core", "dags_folder")
    return DagBag(dag_folder=dags_folder, include_examples=False)
