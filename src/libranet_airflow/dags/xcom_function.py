"""libranet_airflow.dags.xcom_function.

XCom Demo (Function-based)
==========================

Demonstrates automatic XCom passing with TaskFlow API.
Return values are automatically pushed, function arguments automatically pull.

**Source:** `src/libranet_airflow/dags/xcom_function.py`
"""

import datetime as dt

from airflow.sdk import dag, task


@dag(
    dag_id="xcom_function",
    start_date=dt.datetime(2026, 1, 1, tzinfo=dt.UTC),
    schedule=None,
    catchup=False,
    tags={"xcom", "demo"},
    doc_md=__doc__,
)
def xcom_function() -> None:
    """XCom demo using TaskFlow API."""

    @task
    def produce() -> dict:
        """Produce data - return value is automatically pushed to XCom."""
        data = {"name": "Alice", "score": 95}
        print(f"Producing: {data}")
        return data

    @task
    def consume(data: dict) -> str:
        """Consume data - argument is automatically pulled from XCom."""
        message = f"Hello {data['name']}, your score is {data['score']}"
        print(message)
        return message

    # XCom passing happens automatically
    result = produce()
    consume(result)  # type: ignore[arg-type]


dag = xcom_function()
