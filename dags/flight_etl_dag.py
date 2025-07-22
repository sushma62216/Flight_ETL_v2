from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from extract import extract
from transform import transformed_data
from load import load_to_db
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 7, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(dag_id='flight_etl_dag',
        default_args=default_args,
        description='Flight ETL Pipeline',
        schedule_interval='@daily',
        #start_date=datetime(2025,7,8),
        catchup=False,
        tags=['etl','flight','airflow']
        ) as dag:
    
    extract_task=PythonOperator(task_id='extracting_data',
                                python_callable=extract)
    
    transform_task=PythonOperator(task_id='transforming_data',
                                  python_callable=transformed_data)
    
    load_task=PythonOperator(task_id='loading_data',
                             python_callable=load_to_db,
                             provide_context=True)
    
    extract_task>>transform_task>>load_task