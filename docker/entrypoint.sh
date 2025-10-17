#!/bin/sh
set -e

wait_for_db() {
  if [ -n "$DATABASE_URL" ]; then
    HOST=$(python - <<'PY'
from urllib.parse import urlparse
import os
u = urlparse(os.environ["DATABASE_URL"])
print(u.hostname or "db")
PY
)
    PORT=$(python - <<'PY'
from urllib.parse import urlparse
import os
u = urlparse(os.environ["DATABASE_URL"])
print(u.port or 5432)
PY
)
  else
    HOST="${POSTGRES_HOST:-db}"
    PORT="${POSTGRES_PORT:-5432}"
  fi

  echo "Waiting for Postgres at ${HOST}:${PORT} ..."
  until nc -z "$HOST" "$PORT"; do
    sleep 1
  done
  echo "Postgres is up."
}

# czekamy na DB tylko gdy ma sens
if [ -n "$DATABASE_URL" ] || [ -n "$POSTGRES_DB" ] || [ -n "$POSTGRES_HOST" ]; then
  wait_for_db
fi

# statyki sterowane zmiennymi środowiskowymi
[ "$RUN_COLLECTSTATIC" = "1" ] && python manage.py collectstatic --noinput

# odpal właściwą komendę (gunicorn / scrape)
exec "$@"
