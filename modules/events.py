import os
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

def create_event(organizer_id, title, description, event_date, total_capacity):
    """Creates a new event and saves it to the database."""
    # Zorunlu alan kontrolü (Ömer'in auth.py'deki mantığı)
    if not title or not event_date or not total_capacity:
        return {"status": "error", "message": "Başlık, tarih ve kapasite alanları zorunludur!"}

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("""
            INSERT INTO Events (organizer_id, title, description, event_date, total_capacity) 
            VALUES (?, ?, ?, ?, ?)
        """, (organizer_id, title, description, event_date, total_capacity))
        
        conn.commit()
        return {"status": "success", "message": "Etkinlik başarıyla oluşturuldu!"}
    except Exception as e:
        return {"status": "error", "message": f"Etkinlik oluşturulurken hata: {str(e)}"}
    finally:
        conn.close()

def get_active_events():
    """Returns a list of active events for the web view."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("""
            SELECT event_id, organizer_id, title, description, event_date, total_capacity, status 
            FROM Events 
            WHERE status = 'Active'
            ORDER BY event_date ASC
        """)
        rows = cursor.fetchall()
        
        
        events = []
        for row in rows:
            events.append({
                "event_id": row[0],
                "organizer_id": row[1],
                "title": row[2],
                "description": row[3],
                "event_date": row[4],
                "total_capacity": row[5],
                "status": row[6]
            })
        return events
    except Exception as e:
        print(f"Etkinlik Listeleme Hatası: {str(e)}")
        return []
    finally:
        conn.close()