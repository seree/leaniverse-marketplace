# Hetzner Server First-Time Setup

## Step 1: Create the Server in Hetzner Cloud Console

1. Go to https://console.hetzner.cloud
2. Create a new project (or use an existing one)
3. Click **Add Server**:
   - Location: pick closest to your target audience
   - Image: **Ubuntu 22.04 LTS**
   - Type: **CX22** (2 vCPU, 4GB RAM) — good for most early-stage apps
   - SSH Key: add your public key (strongly recommended over password)
   - Name: something descriptive, e.g. `leaniverse-prod`
4. Note the **public IPv4 address** after creation

## Step 2: Point Your Domain to the Server

In your DNS provider (Namecheap, Cloudflare, etc.):
- Add an **A record**: `@` → your server IP
- Add an **A record**: `www` → your server IP
- TTL: 300 (5 minutes) for fast propagation

DNS can take up to 24 hours to fully propagate, but usually works within minutes.

## Step 3: First SSH Login

```bash
ssh root@YOUR_SERVER_IP
```

## Step 4: Create a Non-Root User

Running everything as root is a security risk. Create a deploy user:

```bash
# Create user
adduser deploy

# Add to sudo group
usermod -aG sudo deploy

# Copy SSH key to new user (so you can log in as deploy)
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy
```

Now test login: `ssh deploy@YOUR_SERVER_IP`

From now on, use `deploy` instead of `root`.

## Step 5: Install Docker + Docker Compose

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sudo sh

# Add deploy user to docker group (so you don't need sudo for docker commands)
sudo usermod -aG docker deploy

# Log out and back in for group change to take effect
exit
ssh deploy@YOUR_SERVER_IP

# Verify Docker works
docker --version
docker compose version
```

## Step 6: Configure UFW Firewall

```bash
# Allow SSH (important — do this before enabling UFW!)
sudo ufw allow OpenSSH

# Allow web traffic
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Verify
sudo ufw status
```

## Step 7: Harden SSH (Disable Password Login)

Edit SSH config:

```bash
sudo nano /etc/ssh/sshd_config
```

Find and set these values (uncomment if needed):
```
PasswordAuthentication no
PermitRootLogin no
```

Restart SSH:
```bash
sudo systemctl restart sshd
```

⚠️ Make sure your SSH key login works BEFORE doing this step, or you'll lock yourself out.

## Step 8: Enable Docker to Start on Boot

```bash
sudo systemctl enable docker
```

Your server is now ready for deployment.
