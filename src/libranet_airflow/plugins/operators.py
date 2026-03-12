"""libranet_airflow.plugins.operators."""

from __future__ import annotations

import typing as tp

from airflow.models import BaseOperator

if tp.TYPE_CHECKING:
    from airflow.utils.context import Context


class LibranetOperator(BaseOperator):
    """A Libranet operator that logs a greeting message.

    Operators define a single task in a workflow. They contain the logic
    for what actually gets executed when the task runs.

    Args:
        name: The name to include in the greeting.
        greeting: The greeting prefix. Defaults to "Hello".

    """

    # Fields that should be templated (support Jinja templating)
    template_fields = ("name", "greeting")

    # UI color for this operator in the DAG graph
    ui_color = "#e4f0e8"
    ui_fgcolor = "#000000"

    def __init__(
        self,
        name: str,
        greeting: str = "Hello",
        **kwargs: tp.Any,
    ) -> None:
        """Initialize the operator.

        Args:
            name: The name to include in the greeting.
            greeting: The greeting prefix. Defaults to "Hello".
            **kwargs: Additional arguments passed to BaseOperator.

        """
        super().__init__(**kwargs)
        self.name = name
        self.greeting = greeting

    def execute(self, context: Context) -> str:
        """Execute the operator logic.

        Args:
            context: The Airflow task context containing execution metadata.

        Returns:
            The greeting message (pushed to XCom automatically).

        """
        message = f"{self.greeting}, {self.name}!"
        self.log.info(message)

        # Access context information
        dag_run = context.get("dag_run")
        if dag_run:
            self.log.info("DAG run ID: %s", dag_run.run_id)
            self.log.info("Logical date: %s", dag_run.logical_date)

        # Return value is automatically pushed to XCom
        return message
