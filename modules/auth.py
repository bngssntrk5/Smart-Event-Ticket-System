from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn_str = os.getenv('DB_CONNECTION_STRING')
    return pyodbc.connect(conn_str)

def register_user(username, email, password):
    # Zorunlu alan kontrolü (Required field validation)
    if not username or not email or not password:
        return {"status": "error", "message": "Tüm alanlar zorunlu!"}
    
    # Minimum şifre uzunluğu kontrolü (Minimum password length check)
    if len(password) < 6:
        return {"status": "error", "message": "Şifre en az 6 karakter olmalı!"}

    # Şifreyi hashle (Hash the password)
    hashed_password = generate_password_hash(password, method='scrypt')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Kullanıcıyı veritabanına kaydet (Save user to database)
        cursor.execute(
            "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed_password)
        )
        conn.commit()
        return {"status": "success", "message": "Kayıt başarılı!"}
    except Exception as e:
        print(f"Hata Logu: {e}")
        return {"status": "error", "message": "Kayıt sırasında bir hata oluştu."}
    finally:
        conn.close()

def login_user(email, provided_password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Kullanıcıyı email ile sorgula (Query user by email)
        cursor.execute("SELECT password_hash FROM Users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if user:
            stored_hash = user[0]
            # Hash doğrulaması (Hash verification)
            if check_password_hash(stored_hash, provided_password):
                return {"status": "success", "message": "Giriş başarılı!"}
        
        return {"status": "error", "message": "Email veya şifre hatalı!"}
    except Exception as e:
        print(f"Login Hatası: {e}")
        return {"status": "error", "message": "Giriş işlemi sırasında bir hata oluştu."}
    finally:
        conn.close()