from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="crypto_market_data_pipeline",
    start_date=datetime(2026, 7, 1),
    schedule=None,
    catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_crypto_pipeline",
        bash_command="""
        docker exec crypto_market_data_pipeline python main.py
        """)