from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from functions import extract_data, load_data_to_s3, transform_data_to_postgres

default_args = {
    'owner': 'narwhalhorned',
    'email_on_failure': False,
    'email_on_retry': False,
    'email': ['iztazmn.work@gmail.com'],
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='coinbase_elt_dag_s3_postgres_main_v01',
    default_args=default_args,
    description='Extract, load to S3, and transform data from Coinbase API',
    schedule_interval='0 0 * * *',
    start_date=datetime(2024, 6, 30),
    catchup=True
) as dag:

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_data,
        op_kwargs={'date_for_spot_price': '{{ ds }}'}
    )

    load_to_s3_task = PythonOperator(
        task_id='load_to_s3_task',
        python_callable=load_data_to_s3,
        op_kwargs={'filename': '{{ ti.xcom_pull(task_ids="extract_task") }}', 'current_date': '{{ execution_date.strftime("%Y-%m-%d") }}'}
    )

    transform_to_postgres_task = PythonOperator(
        task_id='transform_to_postgres_task',
        python_callable=transform_data_to_postgres,
        op_args=['{{ ti.xcom_pull(task_ids="load_to_s3_task") }}'],  # Pass S3 key as positional argument
    )

    extract_task >> load_to_s3_task >> transform_to_postgres_task
