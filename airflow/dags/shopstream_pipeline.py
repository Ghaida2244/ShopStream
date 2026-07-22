from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_PATH = "/opt/airflow/shopstream"


with DAG(
    dag_id="shopstream_pipeline",
    start_date=datetime(2026, 7, 22),
    schedule=None,
    catchup=False,
    tags=["shopstream"],
) as dag:

    create_silver = BashOperator(
        task_id="create_silver",
        bash_command=(
            f"cd {PROJECT_PATH} && "
            "python ingestion/create_silver.py"
        ),
    )

    quality_check = BashOperator(
        task_id="quality_check",
        bash_command=(
            f"cd {PROJECT_PATH} && "
            "python ingestion/quality_check.py"
        ),
    )

    create_gold = BashOperator(
        task_id="create_gold",
        bash_command=(
            f"cd {PROJECT_PATH} && "
            "python ingestion/create_gold.py"
        ),
    )

    create_silver >> quality_check >> create_gold