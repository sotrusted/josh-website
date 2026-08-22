#!/bin/bash
set -e
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate --noinput
uv run python manage.py seed

# Create superuser from env vars if set (idempotent — skips if user already exists)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  uv run python manage.py createsuperuser --noinput \
    --username "$DJANGO_SUPERUSER_USERNAME" \
    --email "${DJANGO_SUPERUSER_EMAIL:-admin@joshuashneider.com}" 2>/dev/null || true
fi

exec uv run gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 60
