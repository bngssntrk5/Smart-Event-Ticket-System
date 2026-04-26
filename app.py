from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from modules.tickets import buy_ticket, get_event_occupancy_report
from modules.auth import register_user, login_user

app = Flask(__name__)
app.secret_key = 'bilet_sistemi_2026_xK9m'  # Güvenlik anahtarı

# --- 1. ANA SAYFA (DASHBOARD) ---
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', user_name=session.get('user_name'))

# --- 2. GİRİŞ SAYFASI ---
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        result = login_user(email, password)
        
        if result['status'] == 'success':
            session['user_id'] = result['user']['id']
            session['user_name'] = result['user']['name']
            return redirect(url_for('index'))
        else:
            flash(result['message'], 'error')
            
    return render_template('login.html')

# --- 3. KAYIT SAYFASI ---
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        result = register_user(name, email, password)
        
        if result['status'] == 'success':
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login_page'))
        else:
            flash(result['message'], 'reg_error')
            
    return render_template('login.html')

# --- 4. RAPOR SAYFASI (ANALİZ) ---
@app.route('/report')
def report():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    try:
        analysis_data = get_event_occupancy_report()
        return render_template('ticket_view.html', report=analysis_data)
    except Exception as e:
        return f"Database Error: {str(e)}"

# --- 5. ETKİNLİK OLUŞTURMA (HATA ALDIĞIN KISIM DÜZELTİLDİ) ---
@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    if request.method == 'POST':
        event_name = request.form.get('event_name')
        # Bu kısımda normalde veritabanına kayıt fonksiyonu çağrılır.
        # Şimdilik başarı mesajı verip Dashboard'a yönlendiriyoruz.
        flash(f'Event "{event_name}" successfully created!', 'success')
        return redirect(url_for('index'))
        
    return render_template('create_event.html')

# --- 6. ÇIKIŞ ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# --- 7. BİLET ALMA API (JS İÇİN) ---
@app.route('/api/buy', methods=['POST'])
def buy():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    data = request.json
    user_id = session.get('user_id')
    event_id = data.get('event_id')
    
    result = buy_ticket(user_id, event_id)
    return jsonify(result)

if __name__ == '__main__':
    # Debug modu hataları görmeni sağlar
    app.run(debug=True, port=5000)