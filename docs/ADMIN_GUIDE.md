# ResumeCoach Administrator Guide

**Version:** 1.0  
**Date:** January 8, 2026  
**For:** System Administrators, DevOps Engineers, Technical Support

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Deployment](#deployment)
4. [Configuration](#configuration)
5. [Monitoring & Logging](#monitoring--logging)
6. [Maintenance](#maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Security](#security)
9. [Backup & Recovery](#backup--recovery)
10. [Scaling](#scaling)

---

## 🎯 Overview

### System Components

ResumeCoach consists of three main components:

1. **Backend API** (FastAPI)
   - 10 REST endpoints
   - LLM integration (OpenAI/SageMaker)
   - Resume/Job parsing
   - Session management

2. **Frontend** (Streamlit)
   - 4 pages (Home, Upload, Analysis, Chat)
   - Interactive UI
   - File upload handling

3. **Infrastructure** (AWS)
   - EC2/ECS for hosting
   - S3 for storage (optional)
   - CloudWatch for monitoring
   - RDS for database (optional)

### Technology Stack

- **Python**: 3.10+
- **Backend**: FastAPI 0.109.0
- **Frontend**: Streamlit 1.29.0
- **Web Server**: Nginx + Gunicorn
- **Monitoring**: CloudWatch, System logs
- **Testing**: Pytest (54 tests)

### Access & Credentials

| Component | URL | Credentials |
|-----------|-----|-------------|
| Backend API | https://api.resumecoach.com | No auth (public) |
| API Docs | https://api.resumecoach.com/docs | No auth |
| Frontend | https://app.resumecoach.com | No auth |
| AWS Console | https://console.aws.amazon.com | IAM credentials |
| CloudWatch | https://console.aws.amazon.com/cloudwatch | IAM credentials |
| GitHub | https://github.com/mykh74/resumecoach | SSH key |

---

## 🏗️ Architecture

### System Architecture (EC2 Deployment)

```
┌─────────────────────────────────────────────────────────┐
│                    Internet Users                        │
└───────────────────────┬─────────────────────────────────┘
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
┌──────────────────┐         ┌──────────────────┐
│  Streamlit Cloud │         │  AWS EC2 Instance│
│   (Frontend)     │         │   (Backend API)  │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         │  API calls                 │
         └────────────────────────────┘
                     │
         ┌───────────┴──────────┐
         ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│   OpenAI API     │   │  AWS SageMaker   │
│  (GPT-3.5-turbo) │   │  (Optional LLM)  │
└──────────────────┘   └──────────────────┘
```

### Component Diagram

```
┌─────────────────────────────────────────┐
│         EC2 Instance (t3.medium)        │
│  ┌───────────────────────────────────┐  │
│  │       Nginx (Port 80/443)         │  │
│  │  - Reverse proxy                  │  │
│  │  - SSL termination                │  │
│  │  - Rate limiting                  │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │    Gunicorn + Uvicorn Workers     │  │
│  │  - 4 worker processes             │  │
│  │  - Load balancing                 │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │      FastAPI Application          │  │
│  │  - 10 API endpoints               │  │
│  │  - Business logic                 │  │
│  │  - Session management             │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────┴────────────────────┐  │
│  │      Service Layer                │  │
│  │  - ResumeParser                   │  │
│  │  - JobParser                      │  │
│  │  - LLMService                     │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 🚀 Deployment

### Prerequisites

- AWS account with billing enabled
- Domain name (optional but recommended)
- SSL certificate or Let's Encrypt access
- Git access to repository
- SSH key pair for EC2

### EC2 Deployment (Quick Start)

#### 1. Launch EC2 Instance

```bash
# AMI: Ubuntu 22.04 LTS (ami-0c55b159cbfafe1f0)
# Instance Type: t3.medium (2 vCPU, 4 GB RAM)
# Storage: 20 GB GP3 SSD
# Security Group:
#   - SSH (22) from your IP
#   - HTTP (80) from 0.0.0.0/0
#   - HTTPS (443) from 0.0.0.0/0
#   - Custom TCP (8000) from 0.0.0.0/0 (temporary for testing)
```

#### 2. Connect to Instance

```bash
# Download your key pair (resumecoach-key.pem)
chmod 400 resumecoach-key.pem
ssh -i resumecoach-key.pem ubuntu@<EC2_PUBLIC_IP>
```

#### 3. Run Setup Script

```bash
# On EC2 instance
wget https://raw.githubusercontent.com/mykh74/resumecoach/main/deployment/setup_ec2.sh
chmod +x setup_ec2.sh
./setup_ec2.sh
```

The script will:
- Update system packages
- Install Python, Nginx, dependencies
- Clone repository
- Setup virtual environment
- Configure systemd service
- Setup Nginx reverse proxy
- Optionally configure SSL with Let's Encrypt

#### 4. Configure Environment

```bash
cd /home/ubuntu/resumecoach
nano .env.production
```

**Required variables:**
```bash
# Minimum required
OPENAI_API_KEY=sk-your-actual-key-here
LLM_PROVIDER=openai
ENVIRONMENT=production
API_BASE_URL=https://api.yourdomain.com
ALLOWED_ORIGINS=https://yourstreamlit.streamlit.app
```

#### 5. Start Services

```bash
# Start backend
sudo systemctl start resumecoach-backend
sudo systemctl status resumecoach-backend

# Start Nginx
sudo systemctl restart nginx
sudo systemctl status nginx
```

#### 6. Verify Deployment

```bash
# Test locally
curl http://localhost:8000/api/health

# Test through Nginx
curl http://<EC2_PUBLIC_IP>/api/health

# Run smoke tests
cd /home/ubuntu/resumecoach
./deployment/smoke_test.sh http://<EC2_PUBLIC_IP>
```

### Streamlit Cloud Deployment

#### 1. Push Code to GitHub

```bash
git push origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Configure:
   - Repository: `yourusername/resumecoach`
   - Branch: `main`
   - Main file: `frontend/streamlit_app.py`
   - Python version: 3.10
5. Add secrets:
   ```toml
   API_BASE_URL = "https://api.yourdomain.com"
   ```
6. Click "Deploy"

#### 3. Verify Frontend

Visit: `https://yourusername-resumecoach.streamlit.app`

### Docker Deployment (Alternative)

```bash
# Build image
docker build -t resumecoach:latest .

# Run container
docker run -d \
  --name resumecoach \
  -p 8000:8000 \
  --env-file .env.production \
  resumecoach:latest

# Or use docker-compose
docker-compose up -d
```

---

## ⚙️ Configuration

### Environment Variables

#### Core Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | OpenAI API key for GPT-3.5 |
| `LLM_PROVIDER` | Yes | `openai` | LLM provider (`openai` or `sagemaker`) |
| `ENVIRONMENT` | No | `development` | Environment (`production`, `staging`, `development`) |
| `API_HOST` | No | `0.0.0.0` | API host address |
| `API_PORT` | No | `8000` | API port |
| `API_BASE_URL` | Yes (prod) | - | Public API URL |
| `ALLOWED_ORIGINS` | Yes (prod) | `*` | CORS allowed origins (comma-separated) |

#### AWS Configuration (Optional)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AWS_REGION` | No | `us-east-1` | AWS region |
| `AWS_ACCESS_KEY_ID` | No* | - | AWS access key (*if using SageMaker) |
| `AWS_SECRET_ACCESS_KEY` | No* | - | AWS secret key (*if using SageMaker) |
| `SAGEMAKER_ENDPOINT_NAME` | No | - | SageMaker endpoint name |

#### Application Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `UPLOAD_DIR` | No | `/tmp/uploads` | Upload directory |
| `MAX_UPLOAD_SIZE` | No | `10485760` | Max upload size (bytes) |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `WORKERS` | No | `4` | Number of Gunicorn workers |
| `WORKER_TIMEOUT` | No | `300` | Worker timeout (seconds) |

### Nginx Configuration

Location: `/etc/nginx/sites-available/resumecoach`

#### Key Settings

```nginx
# Rate limiting
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=upload_limit:10m rate=2r/s;

# Client settings
client_max_body_size 10M;

# Timeouts
proxy_connect_timeout 60s;
proxy_send_timeout 300s;
proxy_read_timeout 300s;
```

#### Reload After Changes

```bash
# Test configuration
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

### Systemd Service

Location: `/etc/systemd/system/resumecoach-backend.service`

#### Key Settings

```ini
[Service]
Type=notify
WorkingDirectory=/home/ubuntu/resumecoach
Environment="PATH=/home/ubuntu/resumecoach/venv/bin"
EnvironmentFile=/home/ubuntu/resumecoach/.env.production

ExecStart=/home/ubuntu/resumecoach/venv/bin/gunicorn \
    backend.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 300
```

#### Reload After Changes

```bash
# Reload systemd
sudo systemctl daemon-reload

# Restart service
sudo systemctl restart resumecoach-backend
```

---

## 📊 Monitoring & Logging

### CloudWatch Setup

#### Install CloudWatch Agent

```bash
# Download and install
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Configure
cd /home/ubuntu/resumecoach
./deployment/setup_cloudwatch.sh
```

#### CloudWatch Dashboards

**Default Metrics:**
- CPU utilization
- Memory usage
- Disk usage
- Network I/O
- Request count
- Error rate
- Response time (p50, p95, p99)

**Access:** AWS Console → CloudWatch → Dashboards → ResumeCoach

### Log Files

| Log File | Location | Purpose |
|----------|----------|---------|
| Application | `/var/log/resumecoach/access.log` | API access logs |
| Application | `/var/log/resumecoach/error.log` | API error logs |
| Nginx Access | `/var/log/nginx/access.log` | HTTP access logs |
| Nginx Error | `/var/log/nginx/error.log` | HTTP error logs |
| Systemd | `journalctl -u resumecoach-backend` | Service logs |

#### Viewing Logs

```bash
# Real-time application logs
sudo tail -f /var/log/resumecoach/access.log
sudo tail -f /var/log/resumecoach/error.log

# Real-time Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Systemd logs
sudo journalctl -u resumecoach-backend -f

# Last 100 lines
sudo journalctl -u resumecoach-backend -n 100

# Errors only
sudo journalctl -u resumecoach-backend -p err
```

### Monitoring Commands

```bash
# Service status
sudo systemctl status resumecoach-backend
sudo systemctl status nginx

# Resource usage
htop
free -h
df -h

# Network connections
sudo netstat -tuln | grep 8000
sudo ss -tuln | grep 8000

# Process info
ps aux | grep gunicorn
ps aux | grep nginx

# Check ports
sudo lsof -i :8000
sudo lsof -i :80
sudo lsof -i :443
```

### Alerts & Notifications

#### CloudWatch Alarms

**Recommended Alarms:**

1. **High Error Rate**
   - Metric: 5xx errors
   - Threshold: > 5% of requests
   - Action: SNS notification

2. **High Latency**
   - Metric: Response time p95
   - Threshold: > 10 seconds
   - Action: SNS notification

3. **High CPU**
   - Metric: CPU utilization
   - Threshold: > 80% for 5 minutes
   - Action: SNS notification + scale up

4. **Low Disk Space**
   - Metric: Disk usage
   - Threshold: > 90%
   - Action: SNS notification

5. **Cost Threshold**
   - Metric: Estimated charges
   - Threshold: > $100/month
   - Action: Email notification

#### Setup SNS for Alerts

```bash
# Create SNS topic
aws sns create-topic --name resumecoach-alerts

# Subscribe email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:resumecoach-alerts \
  --protocol email \
  --notification-endpoint admin@resumecoach.com
```

---

## 🔧 Maintenance

### Regular Tasks

#### Daily
- ✅ Check CloudWatch dashboards
- ✅ Review error logs for new issues
- ✅ Verify service health
- ✅ Monitor API response times

#### Weekly
- ✅ Review cost reports
- ✅ Check disk usage
- ✅ Review security groups
- ✅ Update dependencies (if needed)
- ✅ Backup logs

#### Monthly
- ✅ Apply security patches
- ✅ Review and rotate logs
- ✅ Performance optimization review
- ✅ Capacity planning review
- ✅ Update SSL certificates (if manual)

### Common Tasks

#### Restart Backend

```bash
sudo systemctl restart resumecoach-backend
sudo systemctl status resumecoach-backend
```

#### Restart Nginx

```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```

#### Update Code

```bash
cd /home/ubuntu/resumecoach
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart resumecoach-backend
```

#### Update Environment Variables

```bash
cd /home/ubuntu/resumecoach
nano .env.production
sudo systemctl restart resumecoach-backend
```

#### Clear Logs

```bash
# Truncate logs (keep file)
sudo truncate -s 0 /var/log/resumecoach/access.log
sudo truncate -s 0 /var/log/resumecoach/error.log

# Or rotate logs
sudo logrotate /etc/logrotate.d/resumecoach
```

#### Check Application Health

```bash
# Health endpoint
curl http://localhost:8000/api/health

# Full smoke test
cd /home/ubuntu/resumecoach
./deployment/smoke_test.sh http://localhost
```

---

## 🔍 Troubleshooting

### Service Won't Start

**Symptoms:** `systemctl status` shows "failed" or "inactive"

**Debugging:**
```bash
# Check service status
sudo systemctl status resumecoach-backend

# View recent logs
sudo journalctl -u resumecoach-backend -n 50 --no-pager

# Check for port conflicts
sudo lsof -i :8000

# Verify environment file
cat /home/ubuntu/resumecoach/.env.production | grep OPENAI_API_KEY

# Test manual start
cd /home/ubuntu/resumecoach
source venv/bin/activate
gunicorn backend.main:app --bind 0.0.0.0:8000
```

**Common Causes:**
- Missing `.env.production` file
- Invalid `OPENAI_API_KEY`
- Port 8000 already in use
- Python virtual environment not activated
- Missing dependencies

### High Error Rate

**Symptoms:** Many 500 errors in logs

**Debugging:**
```bash
# Check error logs
sudo tail -50 /var/log/resumecoach/error.log

# Check for OpenAI API issues
curl https://status.openai.com/api/v2/status.json

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check memory usage
free -h

# Check CPU usage
top
```

**Common Causes:**
- OpenAI API key expired/invalid
- OpenAI API rate limit exceeded
- Out of memory (OOM)
- High CPU usage
- Network issues

### Slow Response Times

**Symptoms:** Requests taking >10 seconds

**Debugging:**
```bash
# Check system resources
top
htop
df -h

# Check worker processes
ps aux | grep gunicorn

# Test direct API call
time curl http://localhost:8000/api/health

# Check network latency
ping api.openai.com
```

**Solutions:**
- Increase worker count
- Upgrade instance type
- Enable caching
- Optimize database queries (if using DB)

### SSL Certificate Issues

**Symptoms:** HTTPS not working, certificate warnings

**Debugging:**
```bash
# Check certificate
sudo certbot certificates

# Test SSL
openssl s_client -connect api.yourdomain.com:443

# Check Nginx config
sudo nginx -t
```

**Solutions:**
```bash
# Renew certificate
sudo certbot renew

# Force renewal
sudo certbot renew --force-renewal

# Restart Nginx
sudo systemctl restart nginx
```

---

## 🔐 Security

### Security Checklist

#### Server Security
- [ ] SSH key authentication only (no password)
- [ ] Firewall configured (UFW or security groups)
- [ ] Regular security updates
- [ ] Minimal open ports
- [ ] Non-root user for application

#### Application Security
- [ ] HTTPS enforced
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation
- [ ] File upload restrictions
- [ ] No secrets in code
- [ ] Environment variables for credentials

#### AWS Security
- [ ] IAM roles with least privilege
- [ ] MFA enabled
- [ ] CloudTrail logging enabled
- [ ] Security group rules minimized
- [ ] Regular security audits

### Hardening Steps

#### 1. SSH Security

```bash
# Disable password authentication
sudo nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
sudo systemctl restart sshd
```

#### 2. Firewall Setup

```bash
# Install UFW
sudo apt-get install ufw

# Default deny
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443

# Enable
sudo ufw enable
```

#### 3. Fail2Ban

```bash
# Install
sudo apt-get install fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 💾 Backup & Recovery

### Backup Strategy

#### What to Backup
1. **Application Code**: Stored in GitHub (no backup needed)
2. **Configuration**: `.env.production`, Nginx configs
3. **Logs**: CloudWatch + local log files
4. **Data**: User sessions (if persisted to DB)

#### Backup Configuration Files

```bash
# Create backup directory
mkdir -p /home/ubuntu/backups/$(date +%Y%m%d)

# Backup configs
sudo cp /etc/nginx/sites-available/resumecoach /home/ubuntu/backups/$(date +%Y%m%d)/
sudo cp /etc/systemd/system/resumecoach-backend.service /home/ubuntu/backups/$(date +%Y%m%d)/
cp /home/ubuntu/resumecoach/.env.production /home/ubuntu/backups/$(date +%Y%m%d)/

# Create tarball
cd /home/ubuntu
tar -czf backups/resumecoach-$(date +%Y%m%d).tar.gz backups/$(date +%Y%m%d)/

# Upload to S3
aws s3 cp backups/resumecoach-$(date +%Y%m%d).tar.gz \
  s3://resumecoach-backups/configs/
```

#### Automated Backups

Create cron job:
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /home/ubuntu/resumecoach/deployment/backup.sh
```

### Recovery Procedures

#### Recover from Instance Failure

1. Launch new EC2 instance
2. Run setup script
3. Restore configuration files
4. Update DNS
5. Verify functionality

```bash
# Download backup from S3
aws s3 cp s3://resumecoach-backups/configs/resumecoach-20260108.tar.gz .

# Extract
tar -xzf resumecoach-20260108.tar.gz

# Restore configs
sudo cp backups/20260108/nginx.conf /etc/nginx/sites-available/resumecoach
sudo cp backups/20260108/resumecoach-backend.service /etc/systemd/system/
cp backups/20260108/.env.production /home/ubuntu/resumecoach/

# Restart services
sudo systemctl daemon-reload
sudo systemctl restart resumecoach-backend
sudo systemctl restart nginx
```

---

## 📈 Scaling

### Vertical Scaling (Upgrade Instance)

```bash
# Stop application
sudo systemctl stop resumecoach-backend

# Stop instance (AWS Console)
# Change instance type (t3.medium → t3.large)
# Start instance

# Verify
sudo systemctl status resumecoach-backend
```

### Horizontal Scaling (Load Balancer + Auto Scaling)

**Architecture:**
```
Internet → ALB → Target Group → Multiple EC2 Instances
```

**Steps:**
1. Create AMI from current instance
2. Create Launch Template
3. Create Auto Scaling Group (min: 2, max: 10)
4. Create Application Load Balancer
5. Configure health checks
6. Update DNS

### Performance Optimization

#### 1. Increase Workers

```bash
# Edit service file
sudo nano /etc/systemd/system/resumecoach-backend.service

# Change workers count
--workers 8  # Instead of 4

# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart resumecoach-backend
```

#### 2. Enable Caching

```bash
# Install Redis
sudo apt-get install redis-server

# Update .env.production
echo "ENABLE_CACHING=true" >> .env.production
echo "REDIS_URL=redis://localhost:6379/0" >> .env.production

# Restart
sudo systemctl restart resumecoach-backend
```

#### 3. Use CDN

- CloudFront for static assets
- Cache API responses (GET endpoints only)

---

## 📞 Support & Escalation

### Contact Information

| Issue Type | Contact | Response Time |
|------------|---------|---------------|
| Critical (service down) | On-call engineer | <15 min |
| High (degraded performance) | Support team | <1 hour |
| Medium (errors) | Support team | <4 hours |
| Low (questions) | Documentation/email | <24 hours |

### Escalation Path

1. **L1 Support**: Check logs, restart services
2. **L2 Support**: Investigate code issues, check AWS
3. **L3 Support**: Code changes, architecture decisions

---

**Last Updated**: January 8, 2026  
**Version**: 1.0  
**Maintained By**: DevOps Team
