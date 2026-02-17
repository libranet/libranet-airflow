"""libranet_airflow.dags.simple.

Simple DAG
==========

A minimal DAG demonstrating the basic structure.

This DAG contains a single `EmptyOperator` task that does nothing,
useful as a starting template or for testing Airflow connectivity.

**Source:** `src/libranet_airflow/dags/simple.py`
"""

import datetime as dt

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG

with DAG(
    dag_id="simple",
    start_date=dt.datetime(2026, 1, 1, tzinfo=dt.UTC),
    schedule=None,
    catchup=False,
    tags={"simple"},
    doc_md=__doc__,
) as dag:
    EmptyOperator(task_id="hello")
