import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change_this")
API_BASE = os.environ.get("API_BASE", "http://api:8500")

APP_USER = os.environ.get("APP_USER", "admin")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "password")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user == APP_USER and pw == APP_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Main menu after successful login."""
    return render_template('index.html')


@app.route('/employees')
@login_required
def employees():
    resp = requests.get(f"{API_BASE}/employees", params={'limit': 10})
    employees = resp.json() if resp.ok else []
    return render_template('employees.html', employees=employees)


@app.route('/departments')
@login_required
def departments():
    resp = requests.get(f"{API_BASE}/departments")
    departments = resp.json() if resp.ok else []
    return render_template('departments.html', departments=departments)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('certs/server-cert.pem', 'certs/server-key.pem'))
