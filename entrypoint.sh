#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate
pip install -r requirements.txt
poetry install --no-root

echo "PostgreSQL started"

# Ejecutar migraciones
poetry run python manage.py migrate

# Ejecutar el comando que se pase como argumento
exec "$@"