#!/bin/bash
set -e
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate --noinput
uv run python manage.py seed
exec uv run gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 60
