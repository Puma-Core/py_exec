#!/bin/sh
# /Users/facundoveronelli/Documents/puma/django_prog/entrypoint.sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done

# Crear virtual environment si no existe
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "Virtual environment created successfully"
else
    echo "Virtual environment already exists"
fi

echo "Activating virtual environment and installing dependencies..."

# Activar virtual environment y ejecutar comandos dentro de él
.venv/bin/python -m pip install --upgrade pip

# # Si usas requirements.txt
# if [ -f "requirements.txt" ]; then
#     echo "Installing requirements from requirements.txt..."
#     .venv/bin/pip install -r requirements.txt
# fi

# Si usas poetry
if [ -f "pyproject.toml" ]; then
    echo "Installing dependencies with poetry..."
    .venv/bin/python -m pip install poetry
    .venv/bin/poetry install --no-root
fi


echo "PostgreSQL started"

# Ejecutar migraciones usando el virtual environment
# echo "Running migrations..."
# .venv/bin/python manage.py migrate

echo "Starting the application..."
exec "$@"