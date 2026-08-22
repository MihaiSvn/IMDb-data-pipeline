from __future__ import annotations

from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from cosmos import (
    DbtTaskGroup,
    ExecutionConfig,
    ProfileConfig,
    ProjectConfig,
    RenderConfig,
)
from cosmos.constants import TestBehavior

from load_imdb import load_imdb

DBT_PROJECT_PATH = Path("/opt/airflow/dbt")
DBT_PROFILES_YML = DBT_PROJECT_PATH / "profiles.yml"

project_config = ProjectConfig(
    dbt_project_path=DBT_PROJECT_PATH,
)

profile_config = ProfileConfig(
    profile_name="imdb_project",
    target_name="dev",
    profiles_yml_filepath=DBT_PROFILES_YML,
)

execution_config = ExecutionConfig(
    dbt_executable_path="dbt",
)

render_config = RenderConfig(
    test_behavior=TestBehavior.AFTER_EACH,
    exclude=["example"],
)

default_args = {
    "owner": "imdb-team",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="imdb_pipeline_cosmos",
    description="IMDb ELT: Parquet → DuckDB bronze → Cosmos DbtTaskGroup",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    max_active_tasks=1,
    tags=["imdb", "duckdb", "dbt", "cosmos"],
) as dag:
    start = EmptyOperator(task_id="start")

    load = PythonOperator(
        task_id="load_imdb_to_bronze",
        python_callable=load_imdb,
    )

    dbt_transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=render_config,
        operator_args={
            "install_deps": True,
            "append_env": True,
        },
    )

    finish = EmptyOperator(task_id="finish")

    start >> load >> dbt_transform >> finish
