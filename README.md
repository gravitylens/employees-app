# MySQL Server Project

This project sets up an empty MySQL server using Docker. Below are the instructions to get started.

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

## Stopping the Server

To stop the MySQL server, run:

```
docker-compose down
```

## License

This project is licensed under the MIT License.