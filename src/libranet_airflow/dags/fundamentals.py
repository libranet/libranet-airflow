"""libranet_airflow.dags.fundamentals.

Demo DAG: Airflow Fundamentals
==============================

This DAG demonstrates core Airflow concepts for Python developers:

1. DAG definition and scheduling
2. Traditional operators (BashOperator, PythonOperator)
3. TaskFlow API (@task decorator) - the modern, Pythonic approach
4. Task dependencies (>> and <<)
5. XComs - passing data between tasks
6. Branching - conditional task execution
7. Task groups - organizing related tasks
8. Error handling and retries

Run this DAG and explore the Airflow UI to see how tasks execute.
"""

import datetime as dt
import json
import random
import typing as tp

from airflow.models.taskinstance import TaskInstance
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import BranchPythonOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from airflow.sdk import task
from airflow.sdk import task_group

# =============================================================================
# DAG Default Arguments
# =============================================================================
# These apply to all tasks unless overridden at the task level.

default_args = {
    "owner": "airflow",
    "depends_on_past": False,  # Task doesn't wait for previous run's success
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=1),
}


# =============================================================================
# Callable functions (defined outside DAG context)
# =============================================================================


def process_data(ti: TaskInstance, **kwargs: tp.Any) -> str:
    """Process data and push to XCom.

    Args:
        ti: TaskInstance - used for XCom push/pull
        **kwargs: Airflow context (execution_date, dag, etc.)

    Returns:
        Success message.

    """
    # Access execution context
    execution_date = kwargs.get("logical_date")
    print(f"Execution date: {execution_date}")

    # Generate some data
    data = {
        "timestamp": dt.datetime.now(tz=dt.UTC).isoformat(),
        "values": [random.randint(1, 100) for _ in range(5)],  # noqa: S311
        "status": "processed",
    }

    # Push data to XCom for downstream tasks
    ti.xcom_push(key="processed_data", value=data)
    print(f"Pushed data to XCom: {data}")

    return "Success"  # Return value is automatically pushed to XCom


def choose_branch() -> str:
    """Decide which branch to take based on some condition."""
    value = random.choice(["high", "low"])  # noqa: S311
    print(f"Random value: {value}")
    if value == "high":
        return "branch_high"
    return "branch_low"


# =============================================================================
# DAG Definition
# =============================================================================

with DAG(
    dag_id="demo_fundamentals",
    default_args=default_args,
    description="A demo DAG showcasing Airflow fundamentals",
    # Schedule: None = manual trigger only, "@daily", "@hourly", or cron "0 0 * * *"
    schedule=None,
    start_date=dt.datetime(2024, 1, 1, tzinfo=dt.UTC),
    catchup=False,  # Don't backfill missed runs
    tags={"demo", "tutorial"},
    doc_md=__doc__,  # Use module docstring as DAG documentation
) as dag:
    # =========================================================================
    # 1. EMPTY OPERATORS - Workflow markers
    # =========================================================================
    # EmptyOperator (formerly DummyOperator) is useful for:
    # - Marking start/end of workflow sections
    # - Creating join points for parallel tasks

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed")

    # =========================================================================
    # 2. BASH OPERATOR - Run shell commands
    # =========================================================================

    bash_example = BashOperator(
        task_id="bash_example",
        bash_command="""
            echo "Running on $(hostname) at $(date)"
            echo "Python: $(which python)"
            echo "Working directory: $(pwd)"
        """,
    )

    # Bash with environment variables
    bash_with_env = BashOperator(
        task_id="bash_with_env",
        bash_command='echo "Hello, $NAME! Today is $DAY"',
        env={"NAME": "Developer", "DAY": "{{ ds }}"},  # ds = execution date
    )

    # =========================================================================
    # 3. PYTHON OPERATOR - Traditional approach
    # =========================================================================
    # For functions that need to push/pull XCom data manually

    python_operator_example = PythonOperator(
        task_id="python_operator_example",
        python_callable=process_data,
    )

    # =========================================================================
    # 4. TASKFLOW API - Modern Pythonic approach (recommended)
    # =========================================================================
    # Use @task decorator for cleaner code. Return values automatically
    # become XComs, and you can pass them directly between tasks.

    @task
    def extract() -> dict:
        """Extract data from a source (simulated)."""
        data = {
            "users": ["alice", "bob", "charlie"],
            "counts": [10, 25, 15],
            "source": "demo_api",
        }
        print(f"Extracted: {json.dumps(data, indent=2)}")
        return data

    @task
    def transform(raw_data: dict) -> dict:
        """Transform the extracted data."""
        transformed = {
            "user_stats": [
                {"name": user, "count": count, "score": count * 10}
                for user, count in zip(
                    raw_data["users"], raw_data["counts"], strict=True
                )
            ],
            "total": sum(raw_data["counts"]),
            "source": raw_data["source"],
        }
        print(f"Transformed: {json.dumps(transformed, indent=2)}")
        return transformed

    @task
    def load(transformed_data: dict) -> str:
        """Load data to destination (simulated)."""
        print(f"Loading {len(transformed_data['user_stats'])} records...")
        print(f"Total count: {transformed_data['total']}")
        # In reality: write to database, API, file, etc.
        return f"Loaded {transformed_data['total']} items from {transformed_data['source']}"

    # ETL pipeline using TaskFlow - note the clean data passing syntax
    # Note: @task decorated functions return XComArg at definition time
    raw = extract()
    transformed = transform(raw)  # type: ignore[arg-type]
    load_result = load(transformed)  # type: ignore[arg-type]

    # =========================================================================
    # 5. BRANCHING - Conditional execution
    # =========================================================================
    # BranchPythonOperator returns the task_id(s) to execute next.
    # Other downstream tasks are skipped.

    branching = BranchPythonOperator(
        task_id="branching",
        python_callable=choose_branch,
    )

    branch_high = EmptyOperator(task_id="branch_high")
    branch_low = EmptyOperator(task_id="branch_low")

    # Join point after branches - trigger_rule important here
    branch_join = EmptyOperator(
        task_id="branch_join",
        # "none_failed_min_one_success" allows skipped upstream tasks
        trigger_rule="none_failed_min_one_success",
    )

    # =========================================================================
    # 6. TASK GROUPS - Organize related tasks
    # =========================================================================

    @task_group(group_id="validation_group")
    def validation_tasks() -> list:
        """Run validation tasks in parallel."""

        @task
        def validate_schema() -> bool:
            print("Validating schema...")
            return True

        @task
        def validate_completeness() -> bool:
            print("Checking data completeness...")
            return True

        @task
        def validate_quality() -> bool:
            print("Running quality checks...")
            return True

        # These run in parallel within the group
        return [validate_schema(), validate_completeness(), validate_quality()]

    validation_results = validation_tasks()

    # =========================================================================
    # 7. DYNAMIC TASK MAPPING - Generate tasks at runtime
    # =========================================================================

    @task
    def get_partitions() -> list[str]:
        """Return list of partitions to process."""
        return ["partition_a", "partition_b", "partition_c"]

    @task
    def process_partition(partition: str) -> dict:
        """Process a single partition - runs once per partition."""
        print(f"Processing {partition}...")
        return {"partition": partition, "records": random.randint(100, 1000)}  # noqa: S311

    @task
    def summarize(results: list[dict]) -> str:
        """Summarize all partition results."""
        total = sum(r["records"] for r in results)
        print(f"Total records across all partitions: {total}")
        return f"Processed {len(results)} partitions, {total} total records"

    # Dynamic task expansion - creates N tasks based on get_partitions output
    partitions = get_partitions()
    partition_results = process_partition.expand(partition=partitions)
    summary = summarize(partition_results)  # type: ignore[arg-type]

    # =========================================================================
    # 8. TASK DEPENDENCIES
    # =========================================================================
    # >> means "runs before" (downstream)
    # << means "runs after" (upstream)
    # Can also use set_downstream() and set_upstream()

    # Linear dependencies
    start >> bash_example >> bash_with_env >> python_operator_example

    # Parallel branches after python_operator_example
    python_operator_example >> [raw, branching]

    # ETL chain (already connected via TaskFlow)
    load_result >> validation_results >> end

    # Branching flow
    branching >> [branch_high, branch_low] >> branch_join

    # Connect dynamic tasks
    branch_join >> partitions
    summary >> end


# =============================================================================
# KEY CONCEPTS SUMMARY
# =============================================================================
#
# SCHEDULING:
#   - schedule=None: Manual trigger only
#   - schedule="@daily": Run once per day at midnight
#   - schedule="0 6 * * *": Cron syntax (6 AM daily)
#   - schedule=dt.timedelta(hours=1): Every hour
#
# TRIGGER RULES (task.trigger_rule):
#   - "all_success" (default): Run if all parents succeeded
#   - "all_failed": Run if all parents failed
#   - "all_done": Run when all parents are done (any state)
#   - "one_success": Run if at least one parent succeeded
#   - "none_failed": Run if no parent failed (success or skipped OK)
#   - "none_failed_min_one_success": None failed + at least one success
#
# XCOMS (Cross-Communication):
#   - Traditional: ti.xcom_push(key, value) / ti.xcom_pull(task_ids, key)
#   - TaskFlow: Just return values and pass them as function arguments
#
# USEFUL TEMPLATES (Jinja):
#   - {{ ds }}: Execution date (YYYY-MM-DD)
#   - {{ ts }}: Execution timestamp
#   - {{ dag.dag_id }}: DAG ID
#   - {{ task.task_id }}: Task ID
#   - {{ params.my_param }}: Access params dict
#
# =============================================================================
