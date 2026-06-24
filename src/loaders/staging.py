import pandas as pd
import sqlite3  

class StagingLoader:
    def __init__(self, db_path: str = "staging_warehouse.db"):
        self.db_path = db_path

    def load_to_staging(self, df: pd.DataFrame, table_name: str):
        print(f"Loading data into staging table: {table_name}")
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Successfully staged {len(df)} rows into {table_name}.")