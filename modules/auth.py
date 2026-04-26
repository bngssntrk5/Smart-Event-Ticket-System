from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(env_path)

def get_db_connection():
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    driver = os.getenv('DB_DRIVER', '{SQL Server}')
    
    if not server or not database:
        print("!!! HATA: .env dosyasındaki DB_SERVER veya DB_NAME bulunamadı !!!")
        print(f"Aranan .env yolu: {os.path.abspath(env_path)}")
        return None

    conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
    return pyodbc.connect(conn_str)

def register_user(username, email, password):
    if not username or not email or not password:
        return {"status": "error", "message": "Tüm alanlar zorunlu!"}
    
    if len(password) < 6:
        return {"status": "error", "message": "Şifre en az 6 karakter olmalı!"}

    hashed_password = generate_password_hash(password, method='scrypt')
    
    conn = get_db_connection()
    if conn is None: return {"status": "error", "message": "Veritabanı bağlantı hatası!"}
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        return {"status": "success", "message": "Kayıt başarılı!"}
    except Exception as e:
        print(f"Hata Logu: {e}")
        return {"status": "error", "message": f"Kayıt hatası: {e}"}
    finally:
        conn.close()

def login_user(email, provided_password):
    conn = get_db_connection()
    if conn is None: return {"status": "error", "message": "Veritabanı bağlantı hatası!"}
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id, username, password_hash FROM Users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            user_id, username, stored_hash = user
            if check_password_hash(stored_hash, provided_password):
                return {
                    "status": "success",
                    "message": "Giriş başarılı!",
                    "user": {"id": user_id, "name": username}
                }
        
        return {"status": "error", "message": "Email veya şifre hatalı!"}
    except Exception as e:
        print(f"Login Hatası: {e}")
        return {"status": "error", "message": "Giriş hatası oluştu."}
    finally:
        conn.close()