import os
import uuid
import pyodbc
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_db_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    driver = os.getenv('DB_DRIVER', '{SQL Server}')
    conn_str = f"Driver={driver};Server={server};Database={database};Trusted_Connection=yes;"
    return pyodbc.connect(conn_str)

def buy_ticket(user_id, event_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT capacity FROM Events WHERE event_id = ?", (event_id,))
        event = cursor.fetchone()
        if not event: return {"status": "error", "message": "Event not found!"}
        
        cursor.execute("SELECT COUNT(*) FROM Tickets WHERE event_id = ?", (event_id,))
        current_sales = cursor.fetchone()[0]

        if current_sales < event[0]:
            ticket_code = str(uuid.uuid4())[:8].upper()
            cursor.execute("INSERT INTO Tickets (user_id, event_id, ticket_code) VALUES (?, ?, ?)", (user_id, event_id, ticket_code))
            conn.commit()
            return {"status": "success", "code": ticket_code}
        return {"status": "failed", "message": "Event is full!"}
    finally:
        conn.close()

# İŞTE EKSİK OLAN FONKSİYON BU:
def list_all_tickets():
    """Returns a list of all tickets purchased."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT T.ticket_id, U.username, E.event_name, T.ticket_code FROM Tickets T JOIN Users U ON T.user_id = U.user_id JOIN Events E ON T.event_id = E.event_id"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [{"id": r[0], "user": r[1], "event": r[2], "code": r[3]} for r in rows]
    finally:
        conn.close()

def get_event_occupancy_report():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT E.event_name, E.capacity, COUNT(T.ticket_id) FROM Events E LEFT JOIN Tickets T ON E.event_id = T.event_id GROUP BY E.event_name, E.capacity"
        cursor.execute(query)
        rows = cursor.fetchall()
        report = []
        for row in rows:
            rate = (row[2] / row[1]) * 100 if row[1] > 0 else 0
            report.append({"event": row[0], "capacity": row[1], "sold": row[2], "rate": round(rate, 2)})
        return report
    finally:
        conn.close()