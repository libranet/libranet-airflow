"""loader.

DAG loader that imports from the libranet_airflow package.
This file is placed in Airflow's DAGs folder for auto-discovery,
"""

from libranet_airflow.dags import *


# from libranet_airflow.dags import (
#     fundamentals_dag,
#     libranet_dag,
#     simple2_dag,
#     simple_dag,
#     simple_function_dag,
# )

# __all__: list[str] = [
#     "fundamentals_dag",
#     "libranet_dag",
#     "simple2_dag",
#     "simple_dag",
#     "simple_function_dag",
# ]
