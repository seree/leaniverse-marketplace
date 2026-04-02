# Deploying a Next.js App to Hetzner with Docker

## Overview

We'll containerize the Next.js app, run it with Docker Compose, and serve it via nginx with HTTPS.

## Step 1: Dockerfile for Next.js

Create a `Dockerfile` in your project root:

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Copy only what's needed to run
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

> **Note:** The `standalone` output requires `output: 'standalone'` in your `next.config.js`:
> ```js
> module.exports = { output: 'standalone' }
> ```

## Step 2: docker-compose.yml

```yaml
services:
  app:
    build: .
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    expose:
      - "3000"

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

## Step 3: nginx Configuration

Create `nginx.conf` in your project root:

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

    location / {
        proxy_pass http://app:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Replace `YOUR_DOMAIN` with your actual domain.

## Step 4: Get SSL Certificate (First Time)

Before starting the full stack, get a cert using a temporary nginx:

```bash
# Install certbot on the host
sudo apt install certbot -y

# Stop anything using port 80
docker compose down

# Get certificate (standalone mode)
sudo certbot certonly --standalone -d YOUR_DOMAIN -d www.YOUR_DOMAIN

# Certs are saved to /etc/letsencrypt/live/YOUR_DOMAIN/
```

Set up auto-renewal:
```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Step 5: Deploy

```bash
# On your server, in the project directory
git clone YOUR_REPO .   # or rsync from local

# Create .env with production secrets
nano .env

# Build and start
docker compose up -d --build

# Check logs
docker compose logs -f app
```

## Step 6: Verify

```bash
curl -I https://YOUR_DOMAIN
```

Should return `HTTP/2 200`.

## Updating the App

```bash
git pull
docker compose up -d --build
```

## Environment Variables

Next.js has two categories:
- **Server-side only**: put in `.env` — these never leave the server
- **Client-side (public)**: must be prefixed with `NEXT_PUBLIC_` — these are bundled into the JS and visible in the browser. Don't put secrets here.
