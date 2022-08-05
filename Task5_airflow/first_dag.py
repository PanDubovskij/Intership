import pandas as pd
from airflow.models import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from pymongo import MongoClient

review_path = '/home/jan/airflow/dags/tiktok_google_play_reviews.csv'
processed_review_path = '/home/jan/airflow/dags/processed_reviews.csv'


def read_from_csv(ti, path):
    ti.xcom_push(key='path', value=path)
    # df = pd.read_csv(path)


def process(ti, new_path):
    path = ti.xcom_pull(task_ids='get_data', key='path')
    df = pd.read_csv(path)
    df.dropna(how='all', inplace=True)
    df.fillna('-', inplace=True)
    df.sort_values(by=['at'], inplace=True)
    df['content'].replace(r'[^\w\s.,?!]', '', regex=True, inplace=True)
    df.to_csv(new_path)
    ti.xcom_push(key='new_path', value=new_path)


def load_data(ti):
    new_new_path = ti.xcom_pull(task_ids="process_data", key="new_path")
    client = MongoClient("localhost", 2717)
    df = pd.read_csv(new_new_path)
    db = client["airflow_task"]
    db.collection.insert_many(df.to_dict("records"))


with DAG(
        dag_id='reviews_processing',
        start_date=datetime(year=2022, month=7, day=28),
        schedule_interval='@daily',
        catchup=False
) as dag:
    get_data = PythonOperator(
        task_id='get_data',
        python_callable=read_from_csv,
        op_kwargs={'path': review_path}
    )
    #
    process_data = PythonOperator(
        task_id='process_data',
        python_callable=process,
        op_kwargs={'new_path': processed_review_path}
    )
    #
    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load_data
    )

    get_data >> process_data >> load_data
