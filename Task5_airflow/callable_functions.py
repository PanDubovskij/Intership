import pandas as pd
from pymongo import MongoClient


def read_from_csv(ti, path):
    ti.xcom_push(key='path', value=path)
    # df = pd.read_csv(path)


def process_data(ti, new_path):
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
