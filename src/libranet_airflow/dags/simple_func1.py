"""libranet_airflow.dags.simple_func1.

Simple DAG (Function-based)
===========================

A DAG using the modern TaskFlow API with decorators.

Demonstrates:
- @dag decorator instead of DAG context manager
- @task decorator for Python functions
- Automatic XCom passing between tasks

**Source:** `src/libranet_airflow/dags/simple_func1.py`
"""

import datetime as dt

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import dag


@dag(
    dag_id="simple_func1",
    start_date=dt.datetime(2026, 1, 1, tzinfo=dt.UTC),
    schedule=None,
    catchup=False,
    tags={"simple", "taskflow"},
    doc_md=__doc__,
)
def simple_func1() -> None:
    """Define the DAG using TaskFlow API."""
    task_a = EmptyOperator(task_id="task_a")
    task_b = BashOperator(task_id="task_b", bash_command="echo 'Hello from task_b!'")

    task_a >> task_b


# Instantiate the DAG - required for Airflow to discover it
dag = simple_func1()
