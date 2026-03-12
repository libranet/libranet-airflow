"""libranet_airflow.plugins.listeners."""

from __future__ import annotations

import logging
import typing as tp

if tp.TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class LibranetTaskListener:
    """A listener that logs task lifecycle events.

    Listeners allow you to react to events in Airflow without modifying
    the core code. They're useful for monitoring, metrics, and integrations.
    """

    @staticmethod
    def on_task_instance_running(
        previous_state: str,  # noqa: ARG004
        task_instance: TaskInstance,
        session: Session,  # noqa: ARG004
    ) -> None:
        """Log when a task instance starts running."""
        logger.info(
            "[LibranetListener] Task started: %s.%s",
            task_instance.dag_id,
            task_instance.task_id,
        )

    @staticmethod
    def on_task_instance_success(
        previous_state: str,  # noqa: ARG004
        task_instance: TaskInstance,
        session: Session,  # noqa: ARG004
    ) -> None:
        """Log when a task instance succeeds."""
        logger.info(
            "[LibranetListener] Task succeeded: %s.%s (duration: %s)",
            task_instance.dag_id,
            task_instance.task_id,
            task_instance.duration,
        )

    @staticmethod
    def on_task_instance_failed(
        previous_state: str,  # noqa: ARG004
        task_instance: TaskInstance,
        session: Session,  # noqa: ARG004
    ) -> None:
        """Log when a task instance fails."""
        logger.warning(
            "[LibranetListener] Task failed: %s.%s",
            task_instance.dag_id,
            task_instance.task_id,
        )


# Create listener instance
libranet_listener = LibranetTaskListener()
