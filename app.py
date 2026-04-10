from flask import Flask, render_template, request, jsonify
from modules.tickets import buy_ticket, get_event_occupancy_report, list_all_tickets

app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the main dashboard. 
    This page typically shows the list of available events.
    """
    return render_template('dashboard.html')

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