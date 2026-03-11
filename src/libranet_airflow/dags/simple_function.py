"""libranet_airflow.dags.simple_function.

Simple DAG (Function-based)
===========================

A DAG using the modern TaskFlow API with decorators.

Demonstrates:
- @dag decorator instead of DAG context manager
- @task decorator for Python functions
- Automatic XCom passing between tasks

**Source:** `src/libranet_airflow/dags/simple_function.py`
"""

import datetime as dt

from airflow.sdk import dag, task


@dag(
    dag_id="simple_function",
    start_date=dt.datetime(2026, 1, 1, tzinfo=dt.UTC),
    schedule=None,
    catchup=False,
    tags={"simple", "taskflow"},
    doc_md=__doc__,
)
def simple_function() -> None:
    """Define the DAG using TaskFlow API."""

    @task
    def extract() -> dict:
        """Extract data from source."""
        return {"values": [1, 2, 3, 4, 5]}

    @task
    def transform(data: dict) -> dict:
        """Transform the data."""
        total = sum(data["values"])
        return {"total": total, "count": len(data["values"])}

    @task
    def load(result: dict) -> None:
        """Load/print the result."""
        print(f"Total: {result['total']}, Count: {result['count']}")

    # Define task dependencies via function calls
    data = extract()
    result = transform(data)  # type: ignore[arg-type]
    load(result)  # type: ignore[arg-type]


# Instantiate the DAG - required for Airflow to discover it.
# Use a distinct name to avoid shadowing the imported `dag` decorator.
simple_function_dag = simple_function()
