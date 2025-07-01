import os
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'mysql'),
        user=os.environ.get('MYSQL_USER', 'root'),
        password=os.environ.get('MYSQL_PASSWORD', ''),
        database=os.environ.get('MYSQL_DATABASE', 'employees'),
    )

@app.route('/employees', methods=['GET'])
def get_employees():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    limit = int(request.args.get('limit', 10))
    cursor.execute('SELECT emp_no, first_name, last_name, gender, hire_date FROM employees LIMIT %s', (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route('/employees/<int:emp_no>', methods=['GET'])
def get_employee(emp_no):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employees WHERE emp_no = %s', (emp_no,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return jsonify(row)
    return jsonify({'error': 'Employee not found'}), 404

@app.route('/departments', methods=['GET'])
def get_departments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM departments')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
