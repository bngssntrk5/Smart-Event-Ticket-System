import os
import uuid
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes connection to the SQL Server database."""
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    driver = os.getenv('DB_DRIVER', '{SQL Server}')
    
    conn_str = (
        f"Driver={driver};"
        f"Server={server};"
        f"Database={database};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)

def buy_ticket(user_id, event_id):
    """Checks capacity and processes a new ticket purchase."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT capacity FROM Events WHERE event_id = ?", (event_id,))
        event = cursor.fetchone()
        
        if not event: 
            return "Error: Event not found!"
        
        max_capacity = event[0]
        
        cursor.execute("SELECT COUNT(*) FROM Tickets WHERE event_id = ?", (event_id,))
        current_sales = cursor.fetchone()[0]

        if current_sales < max_capacity:
            ticket_code = str(uuid.uuid4())[:8].upper()
            
            cursor.execute(
                "INSERT INTO Tickets (user_id, event_id, ticket_code) VALUES (?, ?, ?)", 
                (user_id, event_id, ticket_code)
            )
            conn.commit()
            return f"SUCCESS! Ticket Code: {ticket_code}"
        else:
            return "FAILED: Event is at full capacity!"
    
    except Exception as e:
        return f"Database Error: {e}"
    finally:
        conn.close()

def list_all_tickets():
    """Displays all purchased tickets with User and Event details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT T.ticket_id, U.user_name, E.event_name, T.ticket_code 
            FROM Tickets T
            JOIN Users U ON T.user_id = U.user_id
            JOIN Events E ON T.event_id = E.event_id
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print("\n" + "="*40)
        print("SYSTEM TICKET LOGS")
        print("="*40)
        for row in rows:
            print(f"ID: {row[0]} | User: {row[1]} | Event: {row[2]} | Code: {row[3]}")
        print("="*40 + "\n")
    finally:
        conn.close()

def get_event_occupancy_report():
    """Analyzes and reports the occupancy rate for each event."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT 
                E.event_name, 
                E.capacity, 
                COUNT(T.ticket_id) as sold_tickets,
                (E.capacity - COUNT(T.ticket_id)) as remaining_slots
            FROM Events E
            LEFT JOIN Tickets T ON E.event_id = T.event_id
            GROUP BY E.event_name, E.capacity
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        print("\n" + "-"*40)
        print("EVENT OCCUPANCY ANALYSIS")
        print("-"*40)
        for row in rows:
            occupancy_rate = (row[2] / row[1]) * 100 if row[1] > 0 else 0
            print(f"Event: {row[0]}")
            print(f"Cap: {row[1]} | Sold: {row[2]} | Remaining: {row[3]}")
            print(f"Occupancy: {occupancy_rate:.2f}%")
            print("-" * 40)
    finally:
        conn.close()

if __name__ == "__main__":
    print("Initiating test transaction...")
    status = buy_ticket(1, 1)
    print(status)
    
    list_all_tickets()
    
    get_event_occupancy_report()