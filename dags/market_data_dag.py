from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# Import  existing logic from the scripts folder
import sys
sys.path.insert(0, '/opt/airflow')
from scripts.extract_load import fetch_and_store

default_args = {
    'owner': 'senior_data_eng',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='market_data_etl_v1',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@hourly', # Runs once an hour
    catchup=False
) as dag:

    # Task 1: Check if CoinGecko is actually up before we try to pull
    check_api = HttpSensor(
        task_id='check_api_availability',
        http_conn_id='http_default', # Define this in Airflow Connections to point to CoinGecko
        endpoint='api/v3/ping',
        poke_interval=30,
        timeout=120
    )

    # Task 2: Run your Python ETL logic
    run_etl = PythonOperator(
        task_id='run_etl_script',
        python_callable=fetch_and_store
    )

    # Task 3: Simple validation to ensure data landed
    validate_db = PostgresOperator(
        task_id='validate_database_count',
        postgres_conn_id='my_postgres_conn',
        sql="SELECT COUNT(*) FROM coin_prices WHERE fetched_at > NOW() - INTERVAL '1 hour';"
    )

    # The Dependency Chain
    check_api >> run_etl >> validate_db