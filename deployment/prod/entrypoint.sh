#!/usr/bin/env bash
set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py createsuperuser --noinput || true

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --threads 2 \
    --timeout 120