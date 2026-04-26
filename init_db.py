import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def init_database():
    print("Connecting to MSSQL...")
    
    conn_str = os.getenv('DB_CONNECTION_STRING')
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("Connected successfully!")

        with open('database.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
            
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print("All tables created successfully in MSSQL!")
        
    except Exception as e:
        print(f"FAILED! Error details: {e}")
    finally:
        if 'conn' in locals():
            conn.close()