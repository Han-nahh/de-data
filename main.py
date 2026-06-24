import os
import yaml
import pandas as pd
from src.extractors.postgres import PostgresExtractor
from src.extractors.sqlserver import SQLServerExtractor
from src.loaders.staging import StagingLoader
from src.transformers.sql_runner import SQLRunner
from src.loaders.snowflake import SnowflakeLoader

def main():
    print("--- Starting ETL Data Integration Pipeline ---")
    os.makedirs("data/processed", exist_ok=True)
    
    with open("config/dummy.yml", "r") as f:
        config = yaml.safe_load(f)
    er_path = config["paths"]["exchange_rates"]
    
    if os.path.exists(er_path):
        er_df = pd.read_csv(er_path)
    else:
        er_df = pd.DataFrame([{"currency": "USD", "rate_to_usd": 1.0}])
    
    pg_extractor = PostgresExtractor()
    ss_extractor = SQLServerExtractor()
    df_pg = pg_extractor.extract()
    df_ss = ss_extractor.extract()
    
    staging_manager = StagingLoader()
    staging_manager.load_to_staging(df_pg, "stg_postgres_sales")
    staging_manager.load_to_staging(df_ss, "stg_sqlserver_sales")
    staging_manager.load_to_staging(er_df, "stg_exchange_rates")
    
    runner = SQLRunner()
    runner.run_script("src/sql/staging_core.sql")
    runner.run_script("src/sql/staging_acquired.sql")
    runner.run_script("src/sql/warehouse_merge.sql")
    
    dw_manager = SnowflakeLoader()
    dw_manager.export_final_tables()
    
    print("--- ETL Pipeline Completed Successfully! ---")

if __name__ == "__main__":
    main()