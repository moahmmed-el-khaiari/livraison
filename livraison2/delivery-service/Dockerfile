# ===== FastAPI Microservice =====
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# (optionnel mais utile) deps système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Installer deps python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Port (tu peux override avec -e PORT=900x)
ENV PORT=9003
EXPOSE 9003

# IMPORTANT: adapte "app.main:app" si ton fichier n’est pas app/main.py
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
