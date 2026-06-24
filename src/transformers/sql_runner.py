import sqlite3
import os

class SQLRunner:
    def __init__(self, db_path: str = "staging_warehouse.db"):
        self.db_path = db_path

    def run_script(self, script_path: str):
        print(f"SQLRunner executing: {script_path}")
        
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"SQL script not found at: {script_path}")
            
        with open(script_path, "r") as f:
            sql_script = f.read()
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            conn.commit()