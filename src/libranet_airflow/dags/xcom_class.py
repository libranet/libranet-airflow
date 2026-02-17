"""libranet_airflow.dags.xcom_class.

XCom Demo (Class-based)
=======================

Demonstrates manual XCom push/pull with PythonOperator.
Use ti.xcom_push() to store and ti.xcom_pull() to retrieve.

**Source:** `src/libranet_airflow/dags/xcom_class.py`
"""

import datetime as dt
import typing as tp

from airflow.models.taskinstance import TaskInstance
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG


def _produce(ti: TaskInstance) -> dict:
    """Produce data and push to XCom manually."""
    data = {"name": "Bob", "score": 87}
    print(f"Producing: {data}")

    # Manual push with custom key
    ti.xcom_push(key="user_data", value=data)

    # Return value is also pushed automatically (key="return_value")
    return data


def _consume(ti: TaskInstance, **kwargs: tp.Any) -> None:
    """Consume data by pulling from XCom manually."""
    # Pull with custom key
    data = ti.xcom_pull(task_ids="produce", key="user_data")
    print(f"Pulled with key 'user_data': {data}")

    # Pull return value (default key)
    data2 = ti.xcom_pull(task_ids="produce")
    print(f"Pulled return value: {data2}")

    message = f"Hello {data['name']}, your score is {data['score']}"
    print(message)


with DAG(
    dag_id="xcom_class",
    start_date=dt.datetime(2026, 1, 1, tzinfo=dt.UTC),
    schedule=None,
    catchup=False,
    tags={"xcom", "demo"},
    doc_md=__doc__,
) as dag:
    produce = PythonOperator(task_id="produce", python_callable=_produce)
    consume = PythonOperator(task_id="consume", python_callable=_consume)

    produce >> consume
