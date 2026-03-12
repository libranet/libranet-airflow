"""loader.

Plugin loader that imports from the libranet_airflow package.
This file is placed in Airflow's plugins folder for auto-discovery,
but the actual plugin code lives in the libranet_airflow-package.
"""

from libranet_airflow.plugins import LibranetAirflowPlugin

__all__: list[str] = ["LibranetAirflowPlugin"]
