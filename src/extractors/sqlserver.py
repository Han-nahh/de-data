import pandas as pd
import yaml
from src.extractors.base_extractor import BaseExtractor

class SQLServerExtractor(BaseExtractor):
    def __init__(self, config_path: str = "config/dummy.yml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            
        self.file_path = config["paths"]["sqlserver_sales"]

    def extract(self) -> pd.DataFrame:
        print(f"Extracting data from SQL Server mock source: {self.file_path}")
        return pd.read_csv(self.file_path)