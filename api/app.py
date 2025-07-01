import os
from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQL_HOST', 'localhost'),
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

@app.route('/departments/<dept_no>', methods=['GET'])
def get_department_detail(dept_no):
    """Return manager and employees for a department"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch basic department info
    cursor.execute('SELECT dept_no, dept_name FROM departments WHERE dept_no=%s', (dept_no,))
    dept = cursor.fetchone()
    if not dept:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Department not found'}), 404

    # Manager information (most recent record)
    cursor.execute('''
        SELECT e.emp_no, e.first_name, e.last_name
        FROM dept_manager dm
        JOIN employees e ON dm.emp_no = e.emp_no
        WHERE dm.dept_no = %s
        ORDER BY dm.to_date DESC
        LIMIT 1
    ''', (dept_no,))
    manager = cursor.fetchone()

    # All employees in the department (current and past)
    cursor.execute('''
        SELECT e.emp_no, e.first_name, e.last_name
        FROM dept_emp de
        JOIN employees e ON de.emp_no = e.emp_no
        WHERE de.dept_no = %s
        ORDER BY e.emp_no
    ''', (dept_no,))
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        'dept_no': dept['dept_no'],
        'dept_name': dept['dept_name'],
        'manager': manager,
        'employees': employees
    })

@app.route('/ping')
def ping():
    return "pong"

@app.route('/salaries/<int:emp_no>', methods=['GET'])
def get_employee_salaries(emp_no):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT e.emp_no, e.first_name, e.last_name, s.salary, s.from_date, s.to_date
        FROM employees e
        JOIN salaries s ON e.emp_no = s.emp_no
        WHERE e.emp_no = %s
        ORDER BY s.from_date DESC
    ''', (emp_no,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    if rows:
        return jsonify(rows)
    return jsonify({'error': 'No salary records found for this employee'}), 404

@app.route('/orgchart', methods=['GET'])
def get_org_chart():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT 
            d.dept_no,
            d.dept_name,
            m.emp_no AS manager_emp_no,
            e.first_name AS manager_first_name,
            e.last_name AS manager_last_name
        FROM departments d
        JOIN dept_manager m ON d.dept_no = m.dept_no
        JOIN employees e ON m.emp_no = e.emp_no
        ORDER BY d.dept_no
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8500)
