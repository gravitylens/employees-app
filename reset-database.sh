#!/bin/bash

# Script to reset the MariaDB database and force rebuild from initialization scripts
# This will delete all existing data and rebuild from ./test_db initialization files

echo "=== MariaDB Database Reset Script ==="
echo "This will:"
echo "1. Stop the database container"
echo "2. Remove all data files"
echo "3. Start the container which will rebuild from ./test_db"
echo ""

# Check if we're in the correct directory
if [ ! -f "docker-compose.yml" ]; then
    echo "Error: Please run this script from the employees-app directory"
    exit 1
fi

read -p "Are you sure you want to delete all database data? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Operation cancelled."
    exit 0
fi

echo ""
echo "Stopping MariaDB container..."
docker-compose stop mysql

echo "Removing data directory..."
rm -rf ./data/*
rm -rf ./data/.*
echo "Note: Keeping the data directory structure"

echo ""
echo "Starting MariaDB container..."
echo "The database will now rebuild from initialization scripts in ./test_db"
docker-compose up -d mysql

echo ""
echo "Database reset complete! The container is now rebuilding from ./test_db"
echo "You can monitor the progress with: docker-compose logs -f mysql"