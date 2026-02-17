"""libranet_airflow.plugins.plugin.

Note: In Airflow 3.0, operators and hooks are no longer registered via plugins.
Import them directly as regular Python modules:
    from libranet_airflow.plugins.operators import LibranetOperator
    from libranet_airflow.plugins.hooks import LibranetHook
"""

from __future__ import annotations

import typing as tp

from airflow.plugins_manager import AirflowPlugin

from libranet_airflow.plugins.listeners import libranet_listener
from libranet_airflow.plugins.macros import libranet_format_date, libranet_greeting


class LibranetAirflowPlugin(AirflowPlugin):
    """Libranet plugin that registers custom components with Airflow.

    The AirflowPlugin class is the entry point for plugins. Airflow
    discovers plugins by looking for subclasses of AirflowPlugin.
    """

    # Unique name for the plugin
    name = "libranet_plugin"

    # Register custom macros (available in Jinja as {{ macros.macro_name() }})
    macros: tp.ClassVar[list[tp.Callable[..., tp.Any]]] = [
        libranet_greeting,
        libranet_format_date,
    ]

    # Register listeners for task lifecycle events
    listeners: tp.ClassVar[list[tp.Any]] = [libranet_listener]
