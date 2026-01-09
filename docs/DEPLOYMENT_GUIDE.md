# ResumeCoach Production Deployment Guide

**Version:** 1.0  
**Date:** January 8, 2026  
**Target:** AWS EC2 + Streamlit Cloud  
**Estimated Time:** 2-3 hours

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [AWS Setup](#aws-setup)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [Verification](#verification)
7. [Post-Deployment](#post-deployment)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This guide walks you through deploying ResumeCoach to production using:
- **Backend**: AWS EC2 (Ubuntu 22.04 with Nginx + Gunicorn)
- **Frontend**: Streamlit Cloud (managed hosting)
- **Monitoring**: AWS CloudWatch
- **Cost**: ~$46/month

### Architecture

```
┌─────────────────┐
│ Streamlit Cloud │
│   (Frontend)    │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│ AWS EC2 Instance│ ← CloudWatch Monitoring
│  Ubuntu 22.04   │
│  ┌───────────┐  │
│  │   Nginx   │  │ ← SSL (Let's Encrypt)
│  │  (Port 80)│  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │ Gunicorn  │  │ ← 4 workers
│  │(Port 8000)│  │
│  └─────┬─────┘  │
│        │        │
│  ┌─────▼─────┐  │
│  │  FastAPI  │  │
│  └───────────┘  │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│   OpenAI API    │
└─────────────────┘
```

---

## ✅ Prerequisites

### Required

1. **AWS Account**
   - Active AWS account
   - Billing enabled
   - Credit card on file

2. **Domain Name** (Optional but recommended)
   - Registered domain (e.g., resumecoach.com)
   - Access to DNS settings

3. **API Keys**
   - OpenAI API key with GPT-3.5-turbo access
   - Sufficient credits ($20+ recommended)

4. **Local Tools**
   - SSH client
   - Git
   - Text editor

5. **GitHub Account**
   - Repository access
   - Push permissions

### Verification Checklist

```bash
# ✅ Check AWS CLI (optional but helpful)
aws --version

# ✅ Check Git
git --version

# ✅ Check SSH
ssh -V

# ✅ Verify OpenAI API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | head -n 20
```

---

## ☁️ AWS Setup

### Step 1: Create IAM User (Optional but Recommended)

1. **Log into AWS Console**: https://console.aws.amazon.com
2. **Navigate to IAM** → Users → Add User
3. **User Details**:
   - Username: `resumecoach-admin`
   - Access type: ✅ Programmatic access, ✅ AWS Management Console
4. **Set Permissions**:
   - Attach policies: `AmazonEC2FullAccess`, `CloudWatchFullAccess`
5. **Download Credentials**: Save access key and secret key

### Step 2: Create EC2 Key Pair

1. **Navigate to EC2** → Key Pairs → Create Key Pair
2. **Key Pair Details**:
   - Name: `resumecoach-key`
   - Key pair type: RSA
   - Format: `.pem` (for Mac/Linux) or `.ppk` (for Windows)
3. **Download** and save to `~/.ssh/resumecoach-key.pem`
4. **Set Permissions**:
   ```bash
   chmod 400 ~/.ssh/resumecoach-key.pem
   ```

### Step 3: Launch EC2 Instance

1. **Navigate to EC2** → Instances → Launch Instance

2. **Name and Tags**:
   - Name: `resumecoach-backend`

3. **Application and OS Images**:
   - AMI: Ubuntu Server 22.04 LTS (HVM)
   - Architecture: 64-bit (x86)

4. **Instance Type**:
   - Type: `t3.medium` (2 vCPU, 4 GB RAM)
   - Cost: ~$0.0416/hour (~$30/month)

5. **Key Pair**:
   - Select: `resumecoach-key`

6. **Network Settings**:
   - VPC: Default
   - Auto-assign Public IP: ✅ Enable
   - Security Group: Create new
     - Name: `resumecoach-sg`
     - Description: Security group for ResumeCoach backend

7. **Security Group Rules**:
   ```
   Type         Protocol  Port Range  Source          Description
   SSH          TCP       22          My IP           SSH access
   HTTP         TCP       80          0.0.0.0/0       HTTP traffic
   HTTPS        TCP       443         0.0.0.0/0       HTTPS traffic
   Custom TCP   TCP       8000        0.0.0.0/0       API (temporary)
   ```

8. **Configure Storage**:
   - Size: 20 GB
   - Volume Type: gp3 (General Purpose SSD)
   - Delete on termination: ✅

9. **Advanced Details** (Optional):
   - Enable CloudWatch detailed monitoring: ✅

10. **Review and Launch**:
    - Click **Launch Instance**
    - Wait 1-2 minutes for instance to start

11. **Get Public IP**:
    - Note your instance's **Public IPv4 address** (e.g., 54.123.45.67)

### Step 4: Set Up Billing Alert

1. **Navigate to CloudWatch** → Alarms → Billing → Create Alarm
2. **Set Threshold**: $100/month
3. **Configure SNS**: Send email alert
4. **Confirm**: Check email and confirm subscription

---

## 🖥️ Backend Deployment

### Step 1: Connect to EC2 Instance

```bash
# Save your EC2 public IP
export EC2_IP="54.123.45.67"  # Replace with your actual IP

# Connect via SSH
ssh -i ~/.ssh/resumecoach-key.pem ubuntu@$EC2_IP
```

**Expected Output**:
```
Welcome to Ubuntu 22.04 LTS (GNU/Linux 5.15.0-1023-aws x86_64)
...
ubuntu@ip-172-31-12-34:~$
```

### Step 2: Run Automated Setup Script

```bash
# Download setup script
wget https://raw.githubusercontent.com/mykh74/resumecoach/main/deployment/setup_ec2.sh

# Make executable
chmod +x setup_ec2.sh

# Run setup (this will take 5-10 minutes)
./setup_ec2.sh
```

**The script will**:
- ✅ Update system packages
- ✅ Install Python 3.10, Nginx, Git, dependencies
- ✅ Clone ResumeCoach repository
- ✅ Set up Python virtual environment
- ✅ Install Python dependencies
- ✅ Prompt for .env.production configuration
- ✅ Create systemd service for backend
- ✅ Configure Nginx reverse proxy
- ✅ Start all services

### Step 3: Configure Environment Variables

When prompted or if editing manually:

```bash
cd /home/ubuntu/resumecoach
nano .env.production
```

**Minimum Required Configuration**:
```bash
# LLM Provider
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
LLM_PROVIDER=openai

# Environment
ENVIRONMENT=production

# API Configuration
API_BASE_URL=http://$EC2_IP  # Or your domain: https://api.resumecoach.com
ALLOWED_ORIGINS=https://your-app.streamlit.app

# Optional
LOG_LEVEL=INFO
WORKERS=4
```

**Save**: `Ctrl+O` → `Enter` → `Ctrl+X`

### Step 4: Start Backend Service

```bash
# Enable and start service
sudo systemctl enable resumecoach-backend
sudo systemctl start resumecoach-backend

# Check status
sudo systemctl status resumecoach-backend
```

**Expected Output**:
```
● resumecoach-backend.service - ResumeCoach FastAPI Backend
     Loaded: loaded (/etc/systemd/system/resumecoach-backend.service; enabled)
     Active: active (running) since Wed 2026-01-08 12:00:00 UTC; 5s ago
   Main PID: 12345 (gunicorn)
      Tasks: 5 (limit: 4644)
     Memory: 250.0M
        CPU: 2.5s
     CGroup: /system.slice/resumecoach-backend.service
             ├─12345 /home/ubuntu/resumecoach/venv/bin/python...
             └─12346 /home/ubuntu/resumecoach/venv/bin/python...
```

### Step 5: Verify Backend

```bash
# Test health endpoint locally
curl http://localhost:8000/api/health
```

**Expected Output**:
```json
{"status":"healthy","timestamp":"2026-01-08T12:00:00Z"}
```

```bash
# Test through Nginx
curl http://localhost/api/health
```

```bash
# Test from outside (your laptop)
curl http://$EC2_IP/api/health
```

### Step 6: Run Smoke Tests

```bash
cd /home/ubuntu/resumecoach
./deployment/smoke_test.sh http://localhost
```

**Expected Output**:
```
🧪 Running Smoke Tests for ResumeCoach
======================================

Testing Health Check... ✓ PASSED (Status: 200)
Testing Root Endpoint... ✓ PASSED (Status: 307)
Testing API Documentation... ✓ PASSED (Status: 200)
Testing Parse Job Description... ✓ PASSED (Status: 200)
...

======================================
Test Summary:
  Passed: 9
  Failed: 0
======================================
✓ All smoke tests passed! 🎉
```

### Step 7: Set Up SSL with Let's Encrypt (Optional but Recommended)

**Prerequisites**: Domain name pointed to EC2 IP

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d api.resumecoach.com
```

**Follow prompts**:
- Email: `admin@resumecoach.com`
- Agree to terms: `Y`
- Share email: `N` (optional)
- Redirect HTTP to HTTPS: `2` (recommended)

**Verify SSL**:
```bash
curl https://api.resumecoach.com/api/health
```

### Step 8: Set Up CloudWatch Monitoring (Optional)

```bash
cd /home/ubuntu/resumecoach
./deployment/setup_cloudwatch.sh
```

**This configures**:
- Application logs → `/aws/resumecoach/access`
- Error logs → `/aws/resumecoach/error`
- System metrics → `ResumeCoach` namespace

---

## 🎨 Frontend Deployment

### Step 1: Prepare Repository

```bash
# On your local machine
cd /path/to/resumecoach

# Ensure all code is committed
git status
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to**: https://share.streamlit.io

2. **Sign In**: Use GitHub account

3. **Click**: "New app"

4. **Configure App**:
   - Repository: `yourusername/resumecoach`
   - Branch: `main`
   - Main file path: `frontend/streamlit_app.py`
   - Advanced settings:
     - Python version: `3.10`

5. **Add Secrets**:
   Click "Advanced settings" → "Secrets"
   
   ```toml
   # Paste this configuration
   API_BASE_URL = "http://54.123.45.67"
   # Or with SSL: API_BASE_URL = "https://api.resumecoach.com"
   ```

6. **Click**: "Deploy!"

7. **Wait**: 2-5 minutes for deployment

8. **Get URL**: Your app will be at `https://yourusername-resumecoach.streamlit.app`

### Step 3: Update Backend CORS

```bash
# SSH back to EC2
ssh -i ~/.ssh/resumecoach-key.pem ubuntu@$EC2_IP

# Update .env.production
cd /home/ubuntu/resumecoach
nano .env.production
```

**Add your Streamlit URL**:
```bash
ALLOWED_ORIGINS=https://yourusername-resumecoach.streamlit.app
```

**Restart backend**:
```bash
sudo systemctl restart resumecoach-backend
```

---

## ✅ Verification

### Complete System Test

```bash
# On your local machine
export API_URL="http://54.123.45.67"  # Or your domain

# Run smoke tests
./deployment/smoke_test.sh $API_URL
```

### Frontend Test

1. **Open**: https://yourusername-resumecoach.streamlit.app
2. **Navigate**: Home → Resume Upload
3. **Upload**: Test resume PDF
4. **Verify**: Resume parsed correctly
5. **Navigate**: Job Analysis
6. **Paste**: Test job description
7. **Verify**: Job parsed correctly
8. **Navigate**: Analysis & Report
9. **Generate**: Analysis report
10. **Verify**: Report generated (10-30 seconds)
11. **Navigate**: Chat with AI
12. **Ask**: Test question
13. **Verify**: Response received

### Load Test (Optional)

```bash
# On your local machine
locust -f locustfile.py --headless \
  -u 10 -r 2 -t 60s \
  --host http://54.123.45.67 \
  --html=reports/production-load-test.html
```

---

## 🔧 Post-Deployment

### Step 1: Document Credentials

**Create a secure document with**:
- EC2 Public IP: `54.123.45.67`
- EC2 Instance ID: `i-0123456789abcdef`
- SSH Key Location: `~/.ssh/resumecoach-key.pem`
- OpenAI API Key: `sk-...` (store securely!)
- Streamlit App URL: `https://yourusername-resumecoach.streamlit.app`
- AWS Console URL: `https://console.aws.amazon.com`

**Store securely**: Password manager (1Password, LastPass, etc.)

### Step 2: Set Up Monitoring Dashboard

1. **Navigate to CloudWatch**: https://console.aws.amazon.com/cloudwatch
2. **Create Dashboard**: "ResumeCoach Production"
3. **Add Widgets**:
   - EC2 CPU Utilization
   - EC2 Memory Usage
   - EC2 Network In/Out
   - Estimated Charges

### Step 3: Create Backup Script

```bash
# On EC2
crontab -e

# Add daily backup at 2 AM UTC
0 2 * * * /home/ubuntu/resumecoach/deployment/backup.sh
```

### Step 4: Set Up Alerts

**CloudWatch Alarms**:
- High CPU (>80% for 5 min) → Email
- High memory (>90%) → Email
- High error rate (>5%) → Email
- Cost exceeds $100/month → Email

### Step 5: Update DNS (If Using Custom Domain)

**Add A Record**:
```
Type: A
Name: api (for api.resumecoach.com)
Value: 54.123.45.67
TTL: 300
```

**Add CNAME (Optional)**:
```
Type: CNAME
Name: www
Value: api.resumecoach.com
TTL: 300
```

### Step 6: Final Security Review

```bash
# SSH to EC2
ssh -i ~/.ssh/resumecoach-key.pem ubuntu@$EC2_IP

# Run security audit
sudo apt-get install lynis
sudo lynis audit system
```

---

## 🔍 Troubleshooting

### Issue: Cannot Connect to EC2

**Check**:
```bash
# Test network connectivity
ping 54.123.45.67

# Test SSH port
nc -zv 54.123.45.67 22

# Verify security group allows your IP
# AWS Console → EC2 → Security Groups → resumecoach-sg
```

**Solution**:
- Update security group to allow your current IP
- Verify key pair permissions: `chmod 400 ~/.ssh/resumecoach-key.pem`

### Issue: Backend Not Starting

**Check logs**:
```bash
# Service status
sudo systemctl status resumecoach-backend

# Recent logs
sudo journalctl -u resumecoach-backend -n 50

# Application logs
sudo tail -50 /var/log/resumecoach/error.log
```

**Common causes**:
- Missing `OPENAI_API_KEY` in `.env.production`
- Port 8000 already in use
- Python dependencies missing

### Issue: Nginx 502 Bad Gateway

**Check**:
```bash
# Test backend directly
curl http://localhost:8000/api/health

# Check Nginx logs
sudo tail -50 /var/log/nginx/error.log

# Verify backend is running
ps aux | grep gunicorn
```

**Solution**:
```bash
# Restart backend
sudo systemctl restart resumecoach-backend

# Restart Nginx
sudo systemctl restart nginx
```

### Issue: Frontend Can't Connect to Backend

**Check CORS**:
```bash
# On EC2, verify ALLOWED_ORIGINS
cat /home/ubuntu/resumecoach/.env.production | grep ALLOWED_ORIGINS
```

**Update CORS**:
```bash
nano /home/ubuntu/resumecoach/.env.production
# Add: ALLOWED_ORIGINS=https://your-app.streamlit.app

sudo systemctl restart resumecoach-backend
```

### Issue: SSL Certificate Failed

**Re-run Certbot**:
```bash
sudo certbot --nginx -d api.resumecoach.com --force-renewal
```

**Check DNS**:
```bash
dig api.resumecoach.com +short
# Should show your EC2 IP
```

---

## 📊 Success Criteria

✅ **Backend**:
- [ ] EC2 instance running
- [ ] Health endpoint returns 200
- [ ] All 10 smoke tests pass
- [ ] SSL configured (if using domain)
- [ ] CloudWatch monitoring active

✅ **Frontend**:
- [ ] Streamlit app accessible
- [ ] Can upload resume
- [ ] Can analyze job
- [ ] Can generate report
- [ ] Can chat with AI

✅ **Integration**:
- [ ] Frontend connects to backend
- [ ] No CORS errors
- [ ] End-to-end workflow works
- [ ] Response times <10s

✅ **Monitoring**:
- [ ] CloudWatch dashboard created
- [ ] Billing alert configured
- [ ] Backup cron job running

---

## 🎉 Deployment Complete!

**Your ResumeCoach is now live!**

- **Backend API**: http://54.123.45.67 (or https://api.resumecoach.com)
- **Frontend**: https://yourusername-resumecoach.streamlit.app
- **API Docs**: http://54.123.45.67/docs
- **Monitoring**: https://console.aws.amazon.com/cloudwatch

### Next Steps

1. **Test thoroughly**: Run through complete user workflow
2. **Monitor costs**: Check AWS billing daily
3. **Gather feedback**: Share with test users
4. **Optimize**: Review performance metrics
5. **Scale**: Consider ECS deployment when traffic increases

### Quick Reference

```bash
# SSH to EC2
ssh -i ~/.ssh/resumecoach-key.pem ubuntu@54.123.45.67

# View logs
sudo journalctl -u resumecoach-backend -f

# Restart backend
sudo systemctl restart resumecoach-backend

# Update code
cd /home/ubuntu/resumecoach
git pull
sudo systemctl restart resumecoach-backend

# Run tests
./deployment/smoke_test.sh http://localhost
```

---

**Last Updated**: January 8, 2026  
**Version**: 1.0  
**Status**: Production Ready 🚀
