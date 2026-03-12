"""libranet_airflow.dags."""

from libranet_airflow.dags.fundamentals import dag as fundamentals_dag
from libranet_airflow.dags.libranet import dag as libranet_dag
from libranet_airflow.dags.simple import dag as simple_dag
from libranet_airflow.dags.simple2 import dag as simple2_dag
from libranet_airflow.dags.simple_func1 import dag as simple_func1_dag
from libranet_airflow.dags.simple_function import dag as simple_function_dag
from libranet_airflow.dags.xcom_class import dag as xcom_class_dag
from libranet_airflow.dags.xcom_function import dag as xcom_function_dag

__all__: list[str] = [
    "fundamentals_dag",
    "libranet_dag",
    "simple2_dag",
    "simple_dag",
    "simple_func1_dag",
    "simple_function_dag",
    "xcom_class_dag",
    "xcom_function_dag",
]
