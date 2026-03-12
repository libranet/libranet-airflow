# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module libranet_airflow.dags.simple."""

import pytest
from airflow.models import DagBag

from libranet_airflow.dags.simple import dag


def test_dag_id() -> None:
    assert dag.dag_id == "simple"


def test_dag_has_one_task() -> None:
    assert len(dag.tasks) == 1


def test_dag_has_hello_task() -> None:
    task_ids = [task.task_id for task in dag.tasks]
    assert "hello" in task_ids


@pytest.mark.integration
def test_airflow_can_load_dag(dag_bag: DagBag) -> None:
    """Integration test: verify Airflow can discover and load the DAG via loader."""
    assert dag_bag.import_errors == {}, f"Import errors: {dag_bag.import_errors}"
    assert "simple" in dag_bag.dags

    loaded_dag = dag_bag.get_dag("simple")
    assert loaded_dag is not None
    assert loaded_dag.dag_id == "simple"
