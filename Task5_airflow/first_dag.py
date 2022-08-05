from airflow.models import DAG, Variable
from datetime import datetime
from airflow.operators.python import PythonOperator
from callable_functions import *

with DAG(
        dag_id='reviews_processing',
        start_date=datetime(year=2022, month=7, day=28),
        schedule_interval='@daily',
        catchup=False
) as dag:
    get_data = PythonOperator(
        task_id='get_data',
        python_callable=read_from_csv,
        op_kwargs={'path': Variable.get('review_path')}
    )
    #
    process_data = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
        op_kwargs={'new_path': Variable.get('processed_review_path')}
    )
    #
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    get_data >> process_data >> load_data
