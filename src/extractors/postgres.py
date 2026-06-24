import pandas as pd
import yaml
from src.extractors.base_extractor import BaseExtractor

class PostgresExtractor(BaseExtractor):
    def __init__(self, config_path: str = "config/dummy.yml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        self.file_path = config["paths"]["postgres_sales"]

    def extract(self) -> pd.DataFrame:
        print(f"Extracting data from Postgres mock source: {self.file_path}")
        return pd.read_csv(self.file_path)