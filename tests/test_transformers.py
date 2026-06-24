import pytest
import sqlite3
import os
from src.transformers.sql_runner import SQLRunner

def test_sql_runner_execution():
    test_db = "test_warehouse.db"
    
    if os.path.exists(test_db):
        try:
            os.remove(test_db)
        except OSError:
            pass

    runner = SQLRunner(db_path=test_db)
    
    conn1 = sqlite3.connect(test_db)
    conn1.execute("CREATE TABLE IF NOT EXISTS test_table (val INT);")
    conn1.commit()
    conn1.close() 
    
    test_script = "test_query.sql"
    with open(test_script, "w") as f:
        f.write("INSERT INTO test_table VALUES (100);")
        
    try:
        runner.run_script(test_script)
        
        conn2 = sqlite3.connect(test_db)
        cursor = conn2.cursor()
        cursor.execute("SELECT * FROM test_table;")
        rows = cursor.fetchall()
        
        cursor.close()
        conn2.close()
        
        assert rows == [(100,)], 
            
    finally:
        if os.path.exists(test_script):
            os.remove(test_script)
        if os.path.exists(test_db):
            try:
                os.remove(test_db)
            except OSError:
                pass