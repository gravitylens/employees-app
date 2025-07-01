# Employees App Docker Environment

  This project provides a ready-to-use MySQL environment with sample data, a REST API, and a web UI, all running in Docker containers with SSL support and remote access.  This application intentionally uses self-signed certificates and exposed secrets to create a training environment in which we can remediate those issues using CyberArk Secrets Manager and CyberArk Certificate Manager.

## Features

- MySQL server in a Docker container
- Sample database and data loaded automatically
- REST API for employee data
- Flask-based web UI
- SSL/TLS enabled with custom certificates
- Remote access enabled (binds to all interfaces)
- Data persisted in a local `data/` directory

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)
- MySQL or MariaDB client (for connecting remotely)
- Python 3.8+ (for running API test scripts)

## Setup

### 1. Clone the repository

```sh
git clone <repo-url>
cd employees-app
```

### 2. Generate SSL Certificates

If not already present, generate SSL certificates in the `certs/` directory for MySQL and in `web/certs/` for the web UI:

```sh
mkdir -p certs
cd certs

# Generate CA key and certificate
openssl genrsa 2048 > ca-key.pem
openssl req -new -x509 -nodes -days 3650 -key ca-key.pem -out ca.pem -subj "/CN=MySQL CA"

# Generate server key and certificate signing request (replace CN as needed)
openssl req -newkey rsa:2048 -days 3650 -nodes -keyout server-key.pem -out server-req.pem -subj "/CN=srv01.cyberarklabs.local"

# Sign server certificate with CA
openssl x509 -req -in server-req.pem -days 3650 -CA ca.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem

cd ..

# Generate a self-signed certificate for the web UI
mkdir -p ../web/certs
openssl req -x509 -newkey rsa:2048 -days 365 -nodes -keyout ../web/certs/server-key.pem -out ../web/certs/server-cert.pem -subj "/CN=web.local"
cd ../..
```

### 3. Configure Environment Variables

Create a `.env` file in the project root (or set these variables in your shell):

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=employees
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
APP_USER=admin
APP_PASSWORD=changeme
SECRET_KEY=your_secret_key
```

### 4. Start the Containers

```sh
docker-compose up -d
```

The server will initialize, load the sample data, and be ready for remote connections.

---

## REST API Documentation

The REST API is served by the Flask app at `http://localhost:8500`.

### Endpoints

#### `GET /employees`
Returns a list of employees.  
**Query Parameters:**
- `limit` (optional): Number of employees to return (default: 10)

**Example:**
```
GET http://localhost:8500/employees?limit=5
```

#### `GET /employees/<emp_no>`
Returns details for a specific employee.

**Example:**
```
GET http://localhost:8500/employees/10001
```

#### `GET /employees/<emp_no>/salaries`
Returns salary history for a specific employee.

**Example:**
```
GET http://localhost:8500/employees/10001/salaries
```

#### `GET /departments`
Returns all departments.

**Example:**
```
GET http://localhost:8500/departments
```

#### `GET /departments/<dept_no>`
Returns department details, manager, and employees.

**Example:**
```
GET http://localhost:8500/departments/d005
```

#### `GET /salaries/<emp_no>`
Returns salary records for a specific employee (alternative to `/employees/<emp_no>/salaries`).

**Example:**
```
GET http://localhost:8500/salaries/10001
```

#### `GET /orgchart`
Returns a list of departments and their current managers.

**Example:**
```
GET http://localhost:8500/orgchart
```

---

## Testing the API

A test script is provided in `api/test_api.py` to quickly check the main endpoints.

### 1. Install dependencies

```sh
cd api
pip install -r requirements.txt
```

### 2. Run the test script

```sh
python test_api.py
```

You can edit `test_api.py` to test additional endpoints or change parameters.

---

## Web UI

The web UI is served over HTTPS at `https://localhost` using self-signed certificates in `web/certs/`.

### Logging In

- **Username:** The value of `APP_USER` in your `.env` file (default: `admin`)
- **Password:** The value of `APP_PASSWORD` in your `.env` file (default: `changeme`)

After logging in, you will see a menu with links to view employees and departments.  
- On the Employees page, click an employee number to view their salary history.
- On the Departments page, click a department number to view its manager and members.

> **Note:** Your browser may warn about the self-signed certificate. You can safely proceed for development purposes.

---

## Database Contents

The server loads the classic MySQL `employees` sample database.  
It contains approximately 300k employee records and related tables describing departments, titles, and salaries.

| Table name   | Description                          |
|--------------|--------------------------------------|
| employees    | Basic information about each employee |
| departments  | List of company departments           |
| dept_manager | Managers for each department          |
| dept_emp     | Mapping between employees and departments |
| titles       | Job titles held by each employee      |
| salaries     | Salary history for employees          |

---

## Running and Stopping the Containers

Start all services:
```sh
docker-compose up -d
```

Stop all services:
```sh
docker-compose down
```

---

## User Permissions

Ensure your MySQL user is allowed to connect from remote hosts (not just `localhost`).  
Example SQL (run inside the container or via a client):

```sql
GRANT ALL PRIVILEGES ON *.* TO 'your_user'@'%' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
```

---

## File Structure

```
.
├── certs/                   # SSL certificates (ca.pem, server-cert.pem, server-key.pem)
├── data/                    # MySQL data directory (ignored by git)
├── test_db/                 # SQL files for schema and data
├── my.cnf                   # MySQL server configuration
├── web/                     # Flask based web UI
├── api/                     # REST API source and test script
├── docker-compose.yml
└── .env                     # Environment variables (not committed)
```

---

## Troubleshooting

- **Connection refused:**  
  Ensure the container is running, port 3306 is open, and firewall rules allow access.

- **SSL/TLS errors:**  
  Ensure you are using the correct CA certificate and client options.

- **Permission denied on certs:**  
  Make sure the cert files exist and have correct permissions.

---

## Authentication

The web UI uses a simple built-in authentication system.  
Default credentials are provided via the `APP_USER` and `APP_PASSWORD` environment variables.  
Sessions are secured using the `SECRET_KEY` environment variable.  
For production, consider integrating a stronger solution such as OAuth2 or connecting to an external identity provider.

---

## License

This project is licensed under the MIT License.  
See individual SQL files for licensing
