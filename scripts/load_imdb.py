"""
Loads raw IMDb files (.tsv.gz), converts them to Parquet
and loads them into the DuckDB 'bronze' schema.
"""

from __future__ import annotations

import os
from pathlib import Path

import duckdb


def _paths() -> tuple[Path, Path]:
    duckdb_path = Path(
        os.environ.get(
            "IMDB_DUCKDB_PATH",
            "/opt/airflow/warehouse/imdb.duckdb",
        )
    )
    data_dir = Path(os.environ.get("IMDB_DATA_DIR", "/opt/airflow/data"))
    return duckdb_path, data_dir


def load_imdb() -> str:
    """
    1. Reads TSVs using IMDb-specific parameters (tab, \\N, no quotes).
    2. Saves as Parquet.
    3. Loads into DuckDB under the bronze schema.
    """
    duckdb_path, data_dir = _paths()
    duckdb_path.parent.mkdir(parents=True, exist_ok=True)

    tables = [
        "title_basics",
        "title_akas",
        "title_crew",
        "title_principals",
        "title_ratings",
        "title_episode",
        "name_basics",
    ]

    con = duckdb.connect(str(duckdb_path))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS bronze")

        for table in tables:
            # Map the table name to the raw file name (e.g., title_basics -> title.basics.tsv.gz)
            file_name = table.replace("_", ".")
            tsv_path = data_dir / f"{file_name}.tsv.gz"
            parquet_path = data_dir / f"{file_name}.parquet"

            if not tsv_path.exists():
                print(f"Raw file not found: {tsv_path}")
                continue

            print(f"Processing {table}...")

            # 1. Export to Parquet
            # We use r"" (raw string) to correctly process the \\N escape
            copy_query = f"""
                COPY (
                    SELECT * FROM read_csv(
                        '{tsv_path}',
                        sep='\\t',
                        header=True,
                        nullstr='\\\\N',
                        quote=''
                    )
                ) TO '{parquet_path}' (FORMAT PARQUET)
            """
            con.execute(copy_query)

            # 2. Create the table in the bronze schema from the clean Parquet file
            load_query = f"""
                CREATE OR REPLACE TABLE bronze.{table} AS
                SELECT * FROM read_parquet('{parquet_path}')
            """
            con.execute(load_query)

            # Log the result
            row_count = con.execute(f"SELECT COUNT(*) FROM bronze.{table}").fetchone()[0]
            print(f"  -> Saved to Parquet and loaded bronze.{table} with {row_count} rows.")

        print(f"Warehouse updated at -> {duckdb_path}")
    finally:
        con.close()

    return str(duckdb_path)


def validate_bronze() -> None:
    """Fails fast if Bronze tables are missing or empty before dbt runs."""
    duckdb_path, _ = _paths()
    if not duckdb_path.exists():
        raise FileNotFoundError(f"DuckDB file not found: {duckdb_path}")

    tables = [
        "title_basics",
        "title_akas",
        "title_crew",
        "title_principals",
        "title_ratings",
        "title_episode",
        "name_basics",
    ]

    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        for table in tables:
            exists = con.execute(
                """
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = 'bronze' AND table_name = ?
                """,
                [table],
            ).fetchone()[0]

            if not exists:
                raise RuntimeError(f"Missing table: bronze.{table}")

            n = con.execute(f"SELECT COUNT(*) FROM bronze.{table}").fetchone()[0]
            if n == 0:
                raise RuntimeError(f"Table bronze.{table} is empty")

            print(f"OK: bronze.{table} has {n} validated rows.")
    finally:
        con.close()
