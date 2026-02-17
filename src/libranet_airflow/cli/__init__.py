"""libranet_airflow.cli."""

import cyclopts

from libranet_airflow.about import version
from libranet_airflow.cli.subcmd1 import app_subcmd1

app: cyclopts.App = cyclopts.App(version=version)

# register subcommands
app.command(obj=app_subcmd1)


@app.default
def main() -> None:
    """Run the main command."""
