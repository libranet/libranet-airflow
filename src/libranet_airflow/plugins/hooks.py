"""libranet_airflow.plugins.hooks."""

from __future__ import annotations

import typing as tp

from airflow.sdk.bases.hook import BaseHook


class LibranetHook(BaseHook):
    """A Libranet hook that simulates connecting to an external system.

    Hooks are interfaces to external platforms and databases. They provide
    a consistent way to connect to services and can be reused across operators.
    """

    conn_name_attr = "libranet_conn_id"
    default_conn_name = "libranet_default"
    conn_type = "libranet"
    hook_name = "Libranet Hook"

    def __init__(self, libranet_conn_id: str = default_conn_name) -> None:
        """Initialize the hook with a connection ID.

        Args:
            libranet_conn_id: The Airflow connection ID to use.

        """
        super().__init__()
        self.libranet_conn_id = libranet_conn_id

    def get_conn(self) -> dict[str, tp.Any]:
        """Return a connection object (simulated).

        In a real hook, this would return an actual connection
        to an external system (database client, API client, etc.).
        """
        connection = self.get_connection(self.libranet_conn_id)
        return {
            "host": connection.host,
            "login": connection.login,
            "schema": connection.schema,
            "extra": connection.extra_dejson,
        }

    def test_connection(self) -> tuple[bool, str]:
        """Test the connection (for UI "Test Connection" button)."""
        try:
            self.get_conn()
        except OSError as e:
            return False, str(e)
        else:
            return True, "Connection successful!"
