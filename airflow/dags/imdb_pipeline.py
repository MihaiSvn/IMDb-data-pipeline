"""
IMDb Data Pipeline — Airflow orchestrates; DuckDB stores; dbt transforms.

Logical stages:
1. Extraction & Loading (load_imdb)
2. Transformation (dbt snapshot & dbt run)
3. Validation (dbt test).
"""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# Import the Python functions we created in scripts/load_imdb.py
from load_imdb import load_imdb, validate_bronze

DBT_DIR = "/opt/airflow/dbt"

# The project requires at least one retry attempt for failed tasks
default_args = {
    "owner": "imdb-pipeline",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="imdb_pipeline",
    description="IMDb ELT: parquet -> DuckDB bronze -> dbt staging/marts",
    default_args=default_args,
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    tags=["imdb", "duckdb", "dbt"],
    doc_md="""
    ### IMDb Data Pipeline

    1. **load_imdb_to_bronze** — Reads TSV, saves as Parquet, and loads into `bronze` schema.
    2. **validate_bronze_tables** — Fails fast if Bronze tables are empty.
    3. **dbt_snapshot** — Captures SCD Type 2 changes on `dim_title`.
    4. **dbt_run** — Runs staging, intermediate, and marts.
    5. **dbt_test** — Runs schema and custom generic tests.
    """,
) as dag:
    start = EmptyOperator(task_id="start")

    # 1. Extraction and Loading
    load = PythonOperator(
        task_id="load_imdb_to_bronze",
        python_callable=load_imdb,
    )

    validate = PythonOperator(
        task_id="validate_bronze_tables",
        python_callable=validate_bronze,
    )

    # 2. Transformation: stratul staging
    dbt_run_staging = BashOperator(
        task_id="dbt_run_staging",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt run --select staging.* --project-dir . --profiles-dir ."
        ),
    )

    # 3. stratul intermediate
    dbt_run_intermediate = BashOperator(
        task_id="dbt_run_intermediate",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt run --select intermediate.* --project-dir . --profiles-dir ."
        ),
    )

    # 4. Snapshot
    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt snapshot --project-dir . --profiles-dir ."
        ),
    )

    # 5. tabelele finale din marts
    dbt_run_marts = BashOperator(
        task_id="dbt_run_marts",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt run --select marts.* --project-dir . --profiles-dir ."
        ),
    )

    # 6. Validation
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            f"cd {DBT_DIR} && "
            "dbt test --project-dir . --profiles-dir ."
        ),
    )

    finish = EmptyOperator(task_id="finish")

    # Logical order
    start >> load >> validate >> dbt_run_staging >> dbt_run_intermediate >> dbt_snapshot >> dbt_run_marts >> dbt_test >> finish
