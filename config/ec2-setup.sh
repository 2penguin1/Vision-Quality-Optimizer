#!/bin/bash

# Image Quality Optimization - EC2 Deployment Setup Script
# This script sets up the environment on a fresh EC2 instance

set -e

echo "=== Image Quality Optimization - EC2 Setup ==="

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker and Docker Compose
echo "Installing Docker..."
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER

# Install Node.js
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python and dependencies
echo "Installing Python and dependencies..."
sudo apt-get install -y python3.10 python3-pip python3-venv
sudo apt-get install -y libopencv-dev python3-opencv

# Clone or download the project (replace with your repo URL)
echo "Setting up project directory..."
mkdir -p /home/ec2-user/image-quality
cd /home/ec2-user/image-quality

# Create necessary directories
mkdir -p logs data

# Set up environment files
echo "Creating environment configuration..."
cat > /home/ec2-user/image-quality/.env << EOF
# MongoDB
MONGODB_URL=mongodb://admin:password@localhost:27017
MONGODB_DB_NAME=image_quality

# JWT
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AWS S3
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_S3_BUCKET=${AWS_S3_BUCKET}
AWS_REGION=${AWS_REGION}

# Server
DEBUG=False
HOST=0.0.0.0
PORT=8000
WORKERS=4
EOF

# Create systemd service files
echo "Creating systemd services..."

# Backend service
sudo tee /etc/systemd/system/image-quality-backend.service > /dev/null << EOF
[Unit]
Description=Image Quality Backend
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
WorkingDirectory=/home/ec2-user/image-quality
ExecStart=/usr/bin/docker-compose -f docker-compose.yml up backend
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Frontend service
sudo tee /etc/systemd/system/image-quality-frontend.service > /dev/null << EOF
[Unit]
Description=Image Quality Frontend
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/ec2-user/image-quality/frontend
ExecStart=$(which npm) run start
Environment="NODE_ENV=production"
Environment="NEXT_PUBLIC_API_URL=http://localhost:8000"
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Install Nginx as reverse proxy
echo "Installing and configuring Nginx..."
sudo apt-get install -y nginx

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/image-quality > /dev/null << 'EOF'
upstream backend {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name _;
    client_max_body_size 50M;

    # API endpoints
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/image-quality /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== Setup Complete ==="
echo "Next steps:"
echo "1. Update .env file with your AWS credentials"
echo "2. Run: sudo systemctl start image-quality-backend"
echo "3. Run: sudo systemctl start image-quality-frontend"
echo "4. Access the application at: http://$(hostname -I | awk '{print $1}')"
