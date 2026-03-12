"""libranet_airflow.plugins.macros."""

from __future__ import annotations

import datetime as dt


def libranet_greeting(name: str) -> str:
    """Generate a greeting message.

    Macros can be used in Jinja templates within DAGs.
    Usage in a DAG: {{ macros.libranet_greeting('World') }}
    """
    return f"Greetings, {name}!"


def libranet_format_date(date: str | dt.datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format a date using the specified format string.

    Usage in a DAG: {{ macros.libranet_format_date(ds, '%d/%m/%Y') }}
    """
    if isinstance(date, str):
        date = dt.datetime.fromisoformat(date)
    return date.strftime(format_str)
