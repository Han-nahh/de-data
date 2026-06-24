import pytest
import pandas as pd
from src.extractors.postgres import PostgresExtractor
from src.extractors.sqlserver import SQLServerExtractor

def test_postgres_extractor_returns_dataframe():
    extractor = PostgresExtractor()
    df = extractor.extract()
    
    assert isinstance(df, pd.DataFrame), "Extractor should return a Pandas DataFrame"
    assert not df.empty, "The extracted Postgres data shouldn't be empty"
    assert 'id' in df.columns, "Postgres data should contain an 'id' column"

def test_sqlserver_extractor_returns_dataframe():
    extractor = SQLServerExtractor()
    df = extractor.extract()
    
    assert isinstance(df, pd.DataFrame), "Extractor should return a Pandas DataFrame"
    assert not df.empty, "The extracted SQL Server data shouldn't be empty"
    assert 'tx_id' in df.columns, "SQL Server data should contain a 'tx_id' column"