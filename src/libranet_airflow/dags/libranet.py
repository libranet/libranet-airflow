"""libranet_airflow.dags.libranet.

Example DAG demonstrating usage of the Libranet plugin.

This DAG shows how to use:
- Custom operators from plugins
- Custom macros from plugins
- Templating with custom macros
"""

import datetime as dt
import logging
import typing as tp

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG

from libranet_airflow.plugins import LibranetOperator
from libranet_airflow.plugins import libranet_format_date
from libranet_airflow.plugins import libranet_greeting

logger = logging.getLogger(__name__)


def print_macro_results(**context: tp.Any) -> None:
    """Print results using custom macros."""
    greeting = libranet_greeting("Plugin User")
    print(f"Macro result: {greeting}")

    # Format the logical date
    logical_date = context["logical_date"]
    formatted = libranet_format_date(logical_date, "%d-%m-%Y")
    print(f"Formatted date: {formatted}")


def read_xcom(**context: tp.Any) -> None:
    """Read XCom value pushed by LibranetOperator."""
    ti = context["ti"]
    greeting = ti.xcom_pull(task_ids="greet_world")
    print(f"Received from XCom: {greeting}")


# DAG definition
with DAG(
    dag_id="libranet_dag",
    description="Example DAG using the Libranet plugin components",
    start_date=dt.datetime(2024, 1, 1, tzinfo=dt.UTC),
    schedule=None,  # Manual trigger only
    catchup=False,
    tags={"libranet", "plugin", "example"},
) as dag:
    # Task 1: Use the custom LibranetOperator
    greet_world = LibranetOperator(
        task_id="greet_world",
        name="World",
        greeting="Hello",
    )

    # Task 2: Use templated fields with the custom operator
    greet_airflow = LibranetOperator(
        task_id="greet_airflow",
        name="{{ dag.dag_id }}",  # Templated field
        greeting="Welcome to",
    )

    # Task 3: Use custom macros in a PythonOperator
    use_macros = PythonOperator(
        task_id="use_macros",
        python_callable=print_macro_results,
    )

    # Task 4: Demonstrate XCom from custom operator
    read_greeting = PythonOperator(
        task_id="read_greeting",
        python_callable=read_xcom,
    )

    # Define task dependencies
    greet_world >> [greet_airflow, read_greeting]
    greet_airflow >> use_macros
