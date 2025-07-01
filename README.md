# MySQL Sample Docker Environment

This project provides a ready-to-use MySQL environment with sample data, SSL support, and remote access using Docker Compose.

## Features

- MySQL server in a Docker container
- Sample database and data loaded automatically
- SSL/TLS enabled with custom certificates
- Remote access enabled (binds to all interfaces)
- Data persisted in a local `data/` directory

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)
- MySQL or MariaDB client (for connecting remotely)

## Setup

### 1. Clone the repository

```sh
git clone <repo-url>
cd mysql-sample
```

### 2. Generate SSL Certificates

If not already present, generate SSL certificates in the `certs/` directory:

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
```

### 3. Configure Environment Variables

Create a `.env` file in the project root (or set these variables in your shell):

```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=employees
MYSQL_USER=your_user
MYSQL_PASSWORD=your_password
```

### 4. Start the MySQL Server

```sh
docker-compose up -d
```

The server will initialize, load the sample data, and be ready for remote connections.

## Connecting Remotely

### Using the MySQL Client

**With SSL (recommended):**

```sh
mysql -h srv01.cyberarklabs.local -u your_user -p --ssl-ca=./certs/ca.pem
```

**With MariaDB Client:**

```sh
mysql -h srv01.cyberarklabs.local -u your_user -p --ssl --ssl-ca=./certs/ca.pem
```

**Without SSL (not recommended for production):**

```sh
mysql -h srv01.cyberarklabs.local -u your_user -p --ssl=0
```

> **Note:**  
> If you see hostname verification errors, use the MariaDB client or the MySQL client with `--ssl-mode=VERIFY_CA` (MySQL 5.7+/8.0+ only).

### User Permissions

Ensure your MySQL user is allowed to connect from remote hosts (not just `localhost`).  
Example SQL (run inside the container or via a client):

```sql
GRANT ALL PRIVILEGES ON *.* TO 'your_user'@'%' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;
```

## File Structure

```
.
├── certs/                   # SSL certificates (ca.pem, server-cert.pem, server-key.pem)
├── data/                    # MySQL data directory (ignored by git)
├── test_db/                 # SQL files for schema and data
├── my.cnf                   # MySQL server configuration
├── docker-compose.yml
└── .env                     # Environment variables (not committed)
```

## Troubleshooting

- **Connection refused:**  
  Ensure the container is running, port 3306 is open, and firewall rules allow access.

- **SSL/TLS errors:**  
  Ensure you are using the correct CA certificate and client options.

- **Permission denied on certs:**  
  Make sure the cert files exist and have correct permissions.

## License

See individual SQL files for licensing