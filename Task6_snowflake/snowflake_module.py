import pandas as pd
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

create_pipeline_sql = """CREATE OR REPLACE TABLE raw_table(
    "_ID" VARCHAR(16777216),
    "IOS_App_Id" NUMBER(38,0),
    "Title" VARCHAR(16777216),
    "Developer_Name" VARCHAR(16777216),
    "Developer_IOS_Id" FLOAT,
    "IOS_Store_Url" VARCHAR(16777216),
    "Seller_Official_Website" VARCHAR(16777216),
    "Age_Rating" VARCHAR(16777216),
    "Total_Average_Rating" FLOAT,
    "Total_Number_of_Ratings" FLOAT,
    "Average_Rating_For_Version" FLOAT,
    "Number_of_Ratings_For_Version" NUMBER(38,0),
    "Original_Release_Date" VARCHAR(16777216),
    "Current_Version_Release_Date" VARCHAR(16777216),
    "Price_USD" FLOAT,
    "Primary_Genre" VARCHAR(16777216),
    "All_Genres" VARCHAR(16777216),
    "Languages" VARCHAR(16777216),
    "Description" VARCHAR(16777216)
    );
    CREATE OR REPLACE TABLE stage_table LIKE raw_table;
    CREATE OR REPLACE TABLE master_table LIKE raw_table;    
    CREATE OR REPLACE STREAM raw_stream ON TABLE raw_table;
    CREATE OR REPLACE STREAM stage_stream ON TABLE stage_table;"""

raw_stage_sql = """INSERT INTO stage_table SELECT "_ID",
            "IOS_App_Id",
            "Title",
            "Developer_Name",
            "Developer_IOS_Id",
            "IOS_Store_Url",
            "Seller_Official_Website",
            "Age_Rating",
            "Total_Average_Rating",
            "Total_Number_of_Ratings",
            "Average_Rating_For_Version",
            "Number_of_Ratings_For_Version",
            "Original_Release_Date",
            "Current_Version_Release_Date",
            "Price_USD",
            "Primary_Genre",
            "All_Genres",
            "Languages",
            "Description"
             FROM raw_stream"""

stage_master_sql = """INSERT INTO master_table SELECT "_ID",
            "IOS_App_Id",
            "Title",
            "Developer_Name",
            "Developer_IOS_Id",
            "IOS_Store_Url",
            "Seller_Official_Website",
            "Age_Rating",
            "Total_Average_Rating",
            "Total_Number_of_Ratings",
            "Average_Rating_For_Version",
            "Number_of_Ratings_For_Version",
            "Original_Release_Date",
            "Current_Version_Release_Date",
            "Price_USD",
            "Primary_Genre",
            "All_Genres",
            "Languages",
            "Description"
             FROM stage_stream"""


def csv_etl_to_raw(path):
    df = pd.read_csv(path)
    connection = SnowflakeHook(snowflake_conn_id='snowflake_conn').get_sqlalchemy_engine().connect()
    step = 9999
    start = 0
    for i in range(df.shape[0] // step + 1):
        df.iloc[start:start + step, :].to_sql("raw_table", con=connection, if_exists='append', index=False)
        start += step
    connection.close()
