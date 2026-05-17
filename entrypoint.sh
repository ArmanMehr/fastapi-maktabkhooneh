#!/bin/bash
# entrypoint.sh

echo "Running database migrations..."
alembic upgrade head

# Start the application
exec "$@"
