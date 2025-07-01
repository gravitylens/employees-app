import requests

BASE_URL = "http://localhost:8500"

def test_get_employees():
    resp = requests.get(f"{BASE_URL}/employees", params={"limit": 3})
    print("GET /employees:", resp.status_code)
    print(resp.json())

def test_get_employee(emp_no):
    resp = requests.get(f"{BASE_URL}/employees/{emp_no}")
    print(f"GET /employees/{emp_no}:", resp.status_code)
    print(resp.json())

def test_get_departments():
    resp = requests.get(f"{BASE_URL}/departments")
    print("GET /departments:", resp.status_code)
    print(resp.json())

if __name__ == "__main__":
    test_get_employees()
    #test_get_employee(10001)  # Replace with a valid emp_no