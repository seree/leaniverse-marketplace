# Deploying a Python App (Django or FastAPI) to Hetzner with Docker

## Overview

We'll containerize the Python app with Docker, serve it via Gunicorn (Django) or Uvicorn (FastAPI), and put nginx in front for HTTPS.

## Dockerfile

### For Django:
```dockerfile
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "YOUR_PROJECT.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
```

Replace `YOUR_PROJECT` with your Django project name (the folder containing `settings.py`).

### For FastAPI:
```dockerfile
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

Replace `main:app` with your module and app instance (e.g., `app.main:app`).

## docker-compose.yml

```yaml
services:
  app:
    build: .
    restart: unless-stopped
    env_file:
      - .env
    expose:
      - "8000"
    volumes:
      - ./media:/app/media  # if using Django file uploads

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - ./staticfiles:/app/staticfiles:ro  # for Django static files
    depends_on:
      - app
```

## nginx Configuration

```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN www.YOUR_DOMAIN;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name YOUR_DOMAIN www.YOUR_DOMAIN;

    ssl_certificate /etc/letsencrypt/live/YOUR_DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/YOUR_DOMAIN/privkey.pem;

    # Serve Django static files directly (skip Python for speed)
    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Remove the `/static/` and `/media/` blocks if using FastAPI (usually not needed).

## Django-Specific: Settings for Production

Make sure `settings.py` has:

```python
DEBUG = False
ALLOWED_HOSTS = ['YOUR_DOMAIN', 'www.YOUR_DOMAIN']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Read SECRET_KEY from environment
import os
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
```

## Required packages

For Django, add to `requirements.txt`:
```
gunicorn
```

For FastAPI:
```
uvicorn[standard]
```

## Get SSL Certificate (First Time)

```bash
# Install certbot on the host
sudo apt install certbot -y

# Stop anything using port 80
docker compose down

# Get certificate
sudo certbot certonly --standalone -d YOUR_DOMAIN -d www.YOUR_DOMAIN

# Enable auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Database: PostgreSQL (Recommended for Django)

Add a database service to `docker-compose.yml`:

```yaml
  db:
    image: postgres:16-alpine
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

In `.env`:
```
POSTGRES_DB=myapp
POSTGRES_USER=myapp_user
POSTGRES_PASSWORD=a-strong-random-password

DATABASE_URL=postgresql://myapp_user:a-strong-random-password@db:5432/myapp
```

Run migrations after first deploy:
```bash
docker compose exec app python manage.py migrate
```

## Deploy

```bash
git clone YOUR_REPO .
nano .env   # fill in secrets

docker compose up -d --build

# Run Django migrations (first time)
docker compose exec app python manage.py migrate

# Check logs
docker compose logs -f app
```

## Updates

```bash
git pull
docker compose up -d --build
docker compose exec app python manage.py migrate  # if there are new migrations
```
