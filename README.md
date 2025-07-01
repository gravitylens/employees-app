# MySQL Server Project

This project sets up a MySQL server containing the classic `employees` sample
database.  It also provides a simple REST API so that the data can be consumed
by other applications.

## Prerequisites

- Docker installed on your machine.
- Docker Compose installed.

## Getting Started

1. Clone the repository:

   ```
   git clone <repository-url>
   cd mysql-server-project
   ```

2. Create a `.env` file in the root directory with the following content:

   ```
   MYSQL_ROOT_PASSWORD=your_root_password
   MYSQL_DATABASE=your_database_name
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   ```

   Replace the placeholders with your desired values.

3. Start the MySQL server using Docker Compose:

   ```
   docker-compose up -d
   ```

4. Access the MySQL server:

   You can connect to the MySQL server using a MySQL client with the following credentials:

   - Host: `localhost`
   - Port: `3306`
   - User: `your_username`
   - Password: `your_password`
   - Database: `your_database_name`

## Database Contents

The server loads the classic MySQL `employees` sample database.  It contains
approximately 300k employee records and related tables describing departments,
titles and salaries.  The main tables are:

| Table name   | Description                          |
|--------------|--------------------------------------|
| employees    | Basic information about each employee |
| departments  | List of company departments           |
| dept_manager | Managers for each department          |
| dept_emp     | Mapping between employees and departments |
| titles       | Job titles held by each employee      |
| salaries     | Salary history for employees          |

## Running the Containers

Start both the MySQL server and the REST API:

```bash
docker-compose up -d
```

The API will be available at `http://localhost:5000`.

## Stopping the Containers

```bash
docker-compose down
```

## License

This project is licensed under the MIT License.
