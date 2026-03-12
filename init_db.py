import sqlite3

def initialize_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    with open('database.sql', 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    try:
        cursor.executescript(sql_script)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()