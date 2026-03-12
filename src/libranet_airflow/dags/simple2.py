"""libranet_airflow.dags.simple2.

Simple2 DAG
===========

A minimal DAG with multiple tasks running every 15 minutes.

Demonstrates:
- Multiple tasks with dependencies
- PythonOperator and BashOperator
- Branching (SmoothOperator only on Mon/Wed/Fri)
- Scheduled execution using timedelta

**Source:** `src/libranet_airflow/dags/simple2.py`
"""

import datetime as dt

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.standard.operators.smooth import SmoothOperator
from airflow.sdk import DAG


def _greet() -> str:
    """Print a greeting message."""
    message = "Hello from simple2!"
    print(message)
    return message


def _choose_smooth_or_skip() -> str:
    """Run SmoothOperator only on Monday, Wednesday, Friday."""
    weekday = dt.datetime.now(tz=dt.UTC).weekday()
    if weekday in (0, 2, 4):  # Mon=0, Wed=2, Fri=4
        return "smooth"
    return "skip_smooth"


with DAG(
    dag_id="simple2",
    start_date=dt.datetime(2026, 1, 1, tzinfo=dt.UTC),
    schedule=dt.timedelta(minutes=15),
    catchup=False,
    tags={"simple"},
    doc_md=__doc__,
) as dag:
    start = EmptyOperator(task_id="start")
    greet = PythonOperator(task_id="greet", python_callable=_greet)
    list_files = BashOperator(task_id="list_files", bash_command="ls -la")
    check_day = BranchPythonOperator(task_id="check_day", python_callable=_choose_smooth_or_skip)
    smooth = SmoothOperator(task_id="smooth")
    skip_smooth = EmptyOperator(task_id="skip_smooth")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

    start >> greet >> list_files >> check_day >> [smooth, skip_smooth] >> end
