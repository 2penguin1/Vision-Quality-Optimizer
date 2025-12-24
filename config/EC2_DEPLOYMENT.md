# Image Quality Optimization - EC2 Deployment Guide

## Prerequisites

- AWS EC2 Instance (Ubuntu 20.04 or 22.04)
- Security Group with ports 80, 443, 8000, 3000 open
- IAM role with S3 access for the EC2 instance
- MongoDB Atlas account (or local MongoDB)

## Quick Start

### 1. SSH into your EC2 instance

```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

### 2. Download and run the setup script

```bash
curl -o setup.sh https://your-repo-url/ec2-setup.sh
chmod +x setup.sh
./setup.sh
```

### 3. Configure Environment Variables

Edit the `.env` file with your actual credentials:

```bash
nano /home/ec2-user/image-quality/.env
```

Update these values:
- `MONGODB_URL`: Your MongoDB connection string
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_S3_BUCKET`: Your S3 bucket name
- `SECRET_KEY`: Keep the auto-generated value

### 4. Start Services

```bash
# Start backend
sudo systemctl start image-quality-backend

# Start frontend
sudo systemctl start image-quality-frontend

# Enable auto-start on reboot
sudo systemctl enable image-quality-backend
sudo systemctl enable image-quality-frontend
```

### 5. Verify Services

```bash
# Check service status
sudo systemctl status image-quality-backend
sudo systemctl status image-quality-frontend

# View logs
sudo journalctl -u image-quality-backend -f
sudo journalctl -u image-quality-frontend -f
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Nginx (Port 80/443)             │
│     Reverse Proxy & Load Balancer       │
├──────────────┬──────────────────────────┤
│              │                          │
v              v                          v
Frontend    Backend              Health Check
(Port 3000) (Port 8000)
│              │
└──────────────┼──────────────────────────┐
               │                          │
               v                          v
          MongoDB              AWS S3 Bucket
         (via Atlas)         (Media Storage)
```

## Performance Tuning

### Backend (FastAPI)

The backend runs with 4 workers by default. Adjust in `.env`:

```
WORKERS=4  # Change based on instance CPU cores
```

For production, use:
```
WORKERS=$(nproc)  # Match number of CPU cores
```

### Frontend (Next.js)

The frontend is built for production. Update in systemd service:

```
NEXT_PUBLIC_API_URL=https://your-domain.com
NODE_ENV=production
```

### Nginx Configuration

Increase worker connections for high traffic:

```bash
sudo nano /etc/nginx/nginx.conf
```

Update:
```
worker_connections 4096;
```

## Monitoring

### CPU and Memory Usage

```bash
top
free -h
```

### Disk Space

```bash
df -h
```

### Service Logs

```bash
# Backend logs
sudo journalctl -u image-quality-backend --no-pager -n 100

# Frontend logs
sudo journalctl -u image-quality-frontend --no-pager -n 100
```

## SSL/TLS Setup (Recommended)

Use Let's Encrypt with Certbot:

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Update Nginx config:
```bash
sudo nano /etc/nginx/sites-available/image-quality
# Add redirect from HTTP to HTTPS
```

## Database Backups

### MongoDB Atlas

1. Enable automated backups in MongoDB Atlas console
2. Configure backup frequency and retention

### Manual Backup

```bash
mongodump --uri="mongodb://user:pass@host:27017/image_quality" --out ./backups
```

## Scaling Considerations

### Horizontal Scaling

1. **Auto Scaling Group**: Create AMI from configured instance
2. **Load Balancer**: Use AWS ELB/ALB in front of instances
3. **Database**: MongoDB Atlas handles horizontal scaling

### Vertical Scaling

- Increase EC2 instance size for more CPU/RAM
- AWS allows stopping instance and changing type
- Update `WORKERS` in backend configuration

## Security Best Practices

1. **Keep SSH key secure** - Never commit to repo
2. **Use IAM roles** - Don't use AWS access keys on EC2
3. **Enable Security Groups** - Restrict port access
4. **Use HTTPS** - Set up SSL certificates
5. **Regular updates** - `sudo apt-get update && upgrade`
6. **Limit MongoDB access** - Use VPC/security groups
7. **Rotate secrets** - Update SECRET_KEY periodically

## Troubleshooting

### Services not starting

```bash
# Check status
sudo systemctl status image-quality-backend

# View errors
sudo journalctl -u image-quality-backend -n 50
```

### MongoDB connection issues

```bash
# Test MongoDB connection
mongo "mongodb://user:pass@host:27017"

# Check connection string in .env
grep MONGODB_URL /home/ec2-user/image-quality/.env
```

### S3 upload failures

1. Verify IAM role has S3 permissions
2. Check bucket exists and region matches
3. Verify CORS configuration on bucket:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST"],
        "AllowedOrigins": ["*"],
        "ExposeHeaders": ["ETag"]
    }
]
```

### Port conflicts

```bash
# Find what's using ports
sudo netstat -tulpn | grep LISTEN
sudo lsof -i :8000
sudo lsof -i :3000
```

## Support

For issues and questions, check the project documentation and logs.
