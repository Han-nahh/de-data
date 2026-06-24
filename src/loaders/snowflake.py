import os
import sqlite3
import yaml
import pandas as pd

class SnowflakeLoader:
    def __init__(self, config_path: str = "config/dummy.yml", db_path: str = "staging_warehouse.db"):
        self.db_path = db_path
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.paths = config["paths"]
        snowflake_config = config["snowflake"]
        self.sf_account = os.environ.get("SNOWFLAKE_ACCOUNT", snowflake_config["account"])
        self.sf_user = os.environ.get("SNOWFLAKE_USER", snowflake_config["user"])
        self.sf_password = os.environ.get("SNOWFLAKE_PASSWORD", snowflake_config["password"])
        self.sf_role = os.environ.get("SNOWFLAKE_ROLE", snowflake_config["role"])
        self.sf_warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", snowflake_config["warehouse"])
        self.sf_database = snowflake_config["database"]
        self.sf_schema = snowflake_config["analytics_schema"]
        print(f"SnowflakeLoader calibrated for account target: {self.sf_account}")

    def export_final_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            df_fact = pd.read_sql_query("SELECT * FROM sales_fact", conn)
            df_fact.to_csv(self.paths["expected_sales_fact"], index=False)
            df_rejects = pd.read_sql_query("SELECT * FROM rejects_fact", conn)
            df_rejects.to_csv(self.paths["expected_rejects"], index=False)