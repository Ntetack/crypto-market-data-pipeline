import requests
import pandas as pd 
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
from cryptomonaie_etl_task import extract_data, create_tables, transform_load_data
import sqlite3



default_args = {
    'owner': 'Lieums',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


with DAG(
    dag_id='crypto_etl_v7',
    schedule='@hourly',
    catchup=False,
    start_date=datetime(2025, 12, 20),
    default_args=default_args,
    tags=['crypto', 'etl', 'coingecko']
) as dag:
    
    start_etl = EmptyOperator(
        task_id='start_etl'
    )

    create_tables_task = PythonOperator(
        task_id='create_tables',
        python_callable=create_tables
    )

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )

    transform_load_task = PythonOperator(
        task_id='transform_load_data',
        python_callable=transform_load_data
    )

    end_etl = EmptyOperator(
        task_id='end_etl'
    )

    start_etl >> extract_task >> transform_load_task >> end_etl

