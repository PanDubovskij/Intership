from airflow.models import DAG, Variable
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
import snowflake_module as sm

with DAG(
        dag_id='snowflake_dag',
        start_date=datetime(year=2022, month=8, day=8),
        schedule_interval='@daily'
) as dag:
    create_pipeline = SnowflakeOperator(
        task_id='create_pipeline',
        snowflake_conn_id='snowflake_conn',
        sql=sm.create_pipeline_sql
    )

    csv_etl_to_raw = PythonOperator(
        task_id='csv_etl_to_raw',
        python_callable=sm.csv_etl_to_raw,
        op_kwargs={'path': Variable.get('ios_apps_info_path')}
    )

    from_raw_to_stage = SnowflakeOperator(
        task_id='from_raw_to_stage',
        snowflake_conn_id='snowflake_conn',
        sql=sm.raw_stage_sql
    )

    from_stage_to_master = SnowflakeOperator(
        task_id='from_stage_to_master',
        snowflake_conn_id='snowflake_conn',
        sql=sm.stage_master_sql
    )
# fsd
    create_pipeline >> csv_etl_to_raw >> from_raw_to_stage >> from_stage_to_master
