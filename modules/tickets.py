import os
import uuid
import pyodbc
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

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
            return {"status": "error", "message": "Event not found!"}
        
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
            return {"status": "success", "message": f"Ticket purchased! Code: {ticket_code}", "code": ticket_code}
        else:
            return {"status": "failed", "message": "Event is full!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

def get_event_occupancy_report():
    """Returns detailed occupancy data for data analysis reports."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT E.event_name, E.capacity, COUNT(T.ticket_id) 
            FROM Events E
            LEFT JOIN Tickets T ON E.event_id = T.event_id
            GROUP BY E.event_name, E.capacity
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        report_data = []
        for row in rows:
            sold = row[2]
            cap = row[1]
            rate = (sold / cap) * 100 if cap > 0 else 0
            report_data.append({
                "event": row[0],
                "capacity": cap,
                "sold": sold,
                "rate": round(rate, 2)
            })
        return report_data
    finally:
        conn.close()