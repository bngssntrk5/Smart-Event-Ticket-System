import pyodbc
import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_db_connection():
    """Veritabanı bağlantısını kurar (Takımın .env standardına uyumlu)"""
    
    conn_str = os.getenv('DB_CONNECTION_STRING')
    
   
    if not conn_str:
        server = os.getenv('DB_SERVER')
        database = os.getenv('DB_NAME')
        driver = os.getenv('DB_DRIVER', '{SQL Server}')
        conn_str = f"Driver={driver};Server={server};Database={database};Trusted_Connection=yes;"
        
    return pyodbc.connect(conn_str)

def get_all_events():
    """Tüm aktif etkinlikleri veritabanından çeker ve arayüze (HTML) gönderir."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("SELECT * FROM Events ORDER BY event_date ASC")
        
        
        columns = [column[0] for column in cursor.description]
        events = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return events
    except Exception as e:
        print(f"Etkinlik Listeleme Hatası: {e}")
        return []
    finally:
        conn.close()

def create_event(organizer_id, title, description, event_date, total_capacity):
    """HTML formundan gelen verilerle yeni bir etkinliği veritabanına kaydeder."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("""
            INSERT INTO Events (organizer_id, title, description, event_date, total_capacity, status)
            VALUES (?, ?, ?, ?, ?, 'Active')
        """, (organizer_id, title, description, event_date, total_capacity))
        
        conn.commit()
        return {"status": "success", "message": "Etkinlik başarıyla oluşturuldu!"}
    except Exception as e:
        print(f"Etkinlik Oluşturma Hatası: {e}")
        return {"status": "error", "message": "Etkinlik oluşturulurken bir hata meydana geldi."}
    finally:
        conn.close()