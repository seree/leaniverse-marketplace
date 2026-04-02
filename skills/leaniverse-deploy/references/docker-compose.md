# Docker Compose Patterns for Leaniverse Deployments

## Common Patterns

### Pattern 1: App + nginx (no database)
Good for: Static-ish apps, apps that use external DB (e.g. PlanetScale, Supabase)
```yaml
services:
  app:
    build: .
    restart: unless-stopped
    env_file: .env
    expose:
      - "3000"  # or 8000 for Python

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - app
```

### Pattern 2: App + PostgreSQL + nginx
Good for: Full-stack apps with a local database
```yaml
services:
  app:
    build: .
    restart: unless-stopped
    env_file: .env
    expose:
      - "8000"
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    env_file: .env
    volumes:
      - postgres_data:/var/lib/postgresql/data

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - app

volumes:
  postgres_data:
```

### Pattern 3: App + Redis (for queues/caching)
```yaml
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

## Useful Commands

```bash
# Start all services in background
docker compose up -d

# Start and rebuild (use after code changes)
docker compose up -d --build

# View logs (all services)
docker compose logs -f

# View logs for one service
docker compose logs -f app

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes database data)
docker compose down -v

# Run a one-off command in a container
docker compose exec app python manage.py migrate
docker compose exec app npm run seed

# Restart a single service
docker compose restart app

# Check container status
docker compose ps

# Pull latest images (for pre-built images)
docker compose pull
```

## .env File Template

```bash
# App
NODE_ENV=production
# or
DJANGO_SETTINGS_MODULE=myproject.settings.production

# Secrets
SECRET_KEY=replace-with-a-long-random-string
DATABASE_URL=postgresql://user:password@db:5432/dbname

# Postgres (if using local db container)
POSTGRES_DB=myapp
POSTGRES_USER=myapp_user
POSTGRES_PASSWORD=replace-with-strong-password

# External services
STRIPE_SECRET_KEY=sk_live_...
SENDGRID_API_KEY=SG...
```

Always add `.env` to `.gitignore`:
```
echo ".env" >> .gitignore
```

## Volume Backup Strategy

For PostgreSQL backups:

```bash
# Dump database to file
docker compose exec db pg_dump -U myapp_user myapp > backup_$(date +%Y%m%d).sql

# Restore from dump
cat backup_20240101.sql | docker compose exec -T db psql -U myapp_user myapp
```

For file uploads (Django media):
```bash
# Simple rsync backup to local machine
rsync -avz deploy@YOUR_SERVER_IP:/path/to/app/media/ ./media-backup/
```
