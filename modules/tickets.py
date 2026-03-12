import os
import uuid
from dotenv import load_dotenv
import pyodbc

load_dotenv() 

def get_db_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    conn_str = (
        f"Driver={{SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def buy_ticket(user_id, event_id):
    conn = get_db_connection()
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
            return f"SUCCESS! Ticket Code: {ticket_code}"
        else:
            return "FAILED: Capacity full!"
    finally:
        conn.close()