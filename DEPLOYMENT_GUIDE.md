# Production Deployment Guide

This guide details how to deploy the **Farmer Crop Advisory Platform** to production environments, including **Docker**, **Render.com**, **AWS EC2**, and **Google Cloud Run**.

---

## 1. Quick Docker Compose Deployment (Easiest for VPS / Any Linux Server)

### Prerequisites:
- Docker Engine $\ge 24.0$
- Docker Compose $\ge 2.20$

### Step 1: Clone Repository & Launch Containers
```bash
git clone https://github.com/your-username/farmer-crop-advisory.git
cd farmer-crop-advisory

# Build and launch both containers in detached background mode
docker-compose up -d --build
```

### Step 2: Verify Running Services
```bash
docker-compose ps
```
- **Frontend:** Accessible at `http://<SERVER_IP>:3000`
- **Backend API:** Accessible at `http://<SERVER_IP>:5000/api/health`

### Step 3: Seed Database Inside Container
```bash
docker exec -it agri_backend python database/seed.py
```

---

## 2. Free Tier Deployment on Render.com

Render provides zero-friction deployment using the included [render.yaml](file:///C:/Users/Rakesh/.gemini/antigravity-ide/scratch/farmer-crop-advisory/render.yaml) blueprint.

### Step 1: Push Code to GitHub
Ensure your repository is pushed to a GitHub or GitLab account.

### Step 2: Create a Blueprint Instance on Render
1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** $\rightarrow$ **Blueprint**.
3. Connect your `farmer-crop-advisory` repository.
4. Render will parse `render.yaml` and configure:
   - **`farmer-advisory-api`** (Python Web Service with Gunicorn).
   - **`farmer-advisory-web`** (Static Site with automatic rewrite rules).
5. Click **Apply**.
6. Once deployed:
   - Backend URL: `https://farmer-advisory-api.onrender.com`
   - Frontend URL: `https://farmer-advisory-web.onrender.com`

---

## 3. Production Deployment on AWS EC2 (Ubuntu 22.04 LTS)

### Step 1: Provision EC2 Instance
- Instance Type: `t3.small` or `t2.medium` (2 vCPU, 2GB RAM minimum for ML inference).
- Security Group: Allow inbound traffic on ports `80` (HTTP), `443` (HTTPS), and `22` (SSH).

### Step 2: Install System Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv nginx git
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### Step 3: Setup Backend with Systemd
1. Clone project:
   ```bash
   cd /var/www
   sudo git clone https://github.com/your-username/farmer-crop-advisory.git
   sudo chown -R ubuntu:ubuntu /var/www/farmer-crop-advisory
   cd farmer-crop-advisory/backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   python database/seed.py
   ```

2. Create Systemd service file:
   ```bash
   sudo nano /etc/systemd/system/agri-backend.service
   ```
   Add:
   ```ini
   [Unit]
   Description=Farmer Crop Advisory Flask Gunicorn Service
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/var/www/farmer-crop-advisory/backend
   Environment="PATH=/var/www/farmer-crop-advisory/backend/.venv/bin"
   Environment="FLASK_ENV=production"
   Environment="PORT=5000"
   Environment="SECRET_KEY=production_secret_key_change_me"
   Environment="JWT_SECRET_KEY=production_jwt_key_change_me"
   ExecStart=/var/www/farmer-crop-advisory/backend/.venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 "app:create_app()"
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Start and enable service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start agri-backend
   sudo systemctl enable agri-backend
   ```

### Step 4: Build and Deploy Frontend
```bash
cd /var/www/farmer-crop-advisory/frontend
npm install
npm run build
```

### Step 5: Configure Nginx as Reverse Proxy
Create site config:
```bash
sudo nano /etc/nginx/sites-available/farmer-advisory
```
Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    root /var/www/farmer-crop-advisory/frontend/dist;
    index index.html;

    # Reverse proxy backend API calls
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SPA routing fallback
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```
Enable site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/farmer-advisory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Setup Free SSL with Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## 4. Google Cloud Run (Serverless Container Deployment)

### Step 1: Install & Initialize Google Cloud SDK
```bash
gcloud auth login
gcloud config set project YOUR_GCP_PROJECT_ID
```

### Step 2: Build & Deploy Backend Container
```bash
cd backend
gcloud builds submit --tag gcr.io/YOUR_GCP_PROJECT_ID/farmer-advisory-backend
gcloud run deploy farmer-advisory-backend \
  --image gcr.io/YOUR_GCP_PROJECT_ID/farmer-advisory-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production,DEMO_MODE=true
```

### Step 3: Deploy Frontend to Firebase Hosting
```bash
cd ../frontend
npm install && npm run build
npx firebase-tools login
npx firebase-tools init hosting
# Set public directory to 'dist' and configure as single-page app: yes
npx firebase-tools deploy --only hosting
```

---

## 5. Production Environment Variables Checklist

| Variable | Description | Recommended Production Value |
| :--- | :--- | :--- |
| `FLASK_ENV` | Runtime mode | `production` |
| `SECRET_KEY` | Flask session cookie secret | 64-char random hex string |
| `JWT_SECRET_KEY` | JWT token signature key | 64-char random hex string |
| `SQLALCHEMY_DATABASE_URI` | Database connection string | `postgresql://user:pass@host:5432/agri_db` |
| `OPENWEATHER_API_KEY` | Real weather forecast key | Your OpenWeatherMap API Key |
| `DEMO_MODE` | Resilient offline mock switch | `false` (set `true` for college demo) |
| `PORT` | Web server listening port | `5000` |
