from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from modules.tickets import buy_ticket, get_event_occupancy_report, list_all_tickets
from modules.auth import register_user, login_user

app = Flask(__name__)
app.secret_key = 'bilet_sistemi_2026_xK9m'  # Session için gizli anahtar (Secret key for session management)

@app.route('/')
def index():
    """
    Renders the main dashboard. 
    This page typically shows the list of available events.
    """
    if 'user_id' not in session:  # Giriş kontrolü (Check if user is logged in)
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', user_name=session.get('user_name'))

# --- AUTH ROUTES ---

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        result = login_user(email, password)  # Auth modülü çağrılıyor (Calling auth module)
        
        if result['status'] == 'success':
            session['user_id'] = result['user']['id']    # Kullanıcı session'a kaydediliyor (Saving user to session)
            session['user_name'] = result['user']['name']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error=result['message'])
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        result = register_user(name, email, password)  # Auth modülü çağrılıyor (Calling auth module)
        
        if result['status'] == 'success':
            return redirect(url_for('login_page'))  # Kayıt sonrası login'e yönlendir (Redirect to login after register)
        else:
            return render_template('login.html', reg_error=result['message'])
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Session temizleniyor (Clearing session)
    return redirect(url_for('login_page'))

# --- TICKET ROUTES ---

@app.route('/report')
def report():
    """
    Fetches real-time occupancy data using SQL and 
    renders it into a professional table for stakeholders.
    """
    try:
        analysis_data = get_event_occupancy_report()
        return render_template('ticket_view.html', report=analysis_data)
    except Exception as e:
        return f"System Error: {str(e)}. Please verify your database configuration (.env)."

@app.route('/api/buy', methods=['POST'])
def buy():
    """
    Endpoint to process ticket purchases. 
    Expects JSON input with user_id and event_id.
    """
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')
    
    if not user_id or not event_id:
        return jsonify({"status": "error", "message": "Required parameters missing."}), 400
    
    result = buy_ticket(user_id, event_id)
    return jsonify(result)

@app.route('/api/tickets')
def all_tickets():
    """Returns all ticket records in JSON format for external reporting."""
    tickets = list_all_tickets()
    return jsonify(tickets)

if __name__ == '__main__':
    app.run(debug=True, port=5000)