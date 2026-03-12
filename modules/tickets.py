import os
from dotenv import load_dotenv
import pyodbc

load_dotenv()

def get_connection():
    return pyodbc.connect(
        f"Driver={{SQL Server}};"
        f"Server={os.getenv('DB_SERVER')};"
        f"Database={os.getenv('DB_NAME')};"
        "Trusted_Connection=yes;"
    )
    
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT capacity FROM Events WHERE event_id = ?", (event_id,))
        event = cursor.fetchone()
        
        if not event: return "Error: Event not found!"
        
        capacity = event[0]
        cursor.execute("SELECT COUNT(*) FROM Tickets WHERE event_id = ?", (event_id,))
        current_tickets = cursor.fetchone()[0]

        if current_tickets < capacity:
            ticket_code = str(uuid.uuid4())[:8].upper()
            cursor.execute("INSERT INTO Tickets (user_id, event_id, ticket_code) VALUES (?, ?, ?)", 
                           (user_id, event_id, ticket_code))
            conn.commit()
            return f"SUCCESS! Code: {ticket_code}"
        else:
            return "FAILED: Capacity full!"
    finally:
        conn.close()