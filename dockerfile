# ---- Baza obrazu ----
FROM python:3.12-slim

# ---- Ustawienia Pythona ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ---- Katalog roboczy ----
WORKDIR /app

# ---- Systemowe zależności (libpq do psycopg, netcat do wait-on-db, build tools do kompilacji) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
 && rm -rf /var/lib/apt/lists/*

# ---- Kopiowanie zależności i instalacja (lepsze cache) ----
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN python -m playwright install --with-deps chromium

# ---- Reszta kodu ----
COPY . /app

# ---- Uprawnienia i entrypoint ----
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]
