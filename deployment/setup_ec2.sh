#!/bin/bash
# EC2 Setup Script for ResumeCoach
# Run this script on a fresh Ubuntu 22.04 EC2 instance

set -e  # Exit on any error

echo "🚀 Starting ResumeCoach Backend Deployment on EC2"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="resumecoach"
APP_DIR="/home/ubuntu/$APP_NAME"
REPO_URL="https://github.com/mykh74/resumecoach.git"
PYTHON_VERSION="3.10"

# Function to print colored messages
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_error "Please do not run as root (no sudo). Run as ubuntu user."
    exit 1
fi

print_status "Step 1: Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq

print_status "Step 2: Installing system dependencies..."
sudo apt-get install -y \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python3-pip \
    nginx \
    git \
    curl \
    build-essential \
    libpoppler-cpp-dev \
    certbot \
    python3-certbot-nginx

print_status "Step 3: Cloning repository..."
if [ -d "$APP_DIR" ]; then
    print_info "Directory exists, pulling latest changes..."
    cd "$APP_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

print_status "Step 4: Setting up Python virtual environment..."
python${PYTHON_VERSION} -m venv venv
source venv/bin/activate

print_status "Step 5: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server

print_status "Step 6: Setting up environment variables..."
if [ ! -f .env.production ]; then
    cp .env.production.example .env.production
    print_info "Created .env.production file. Please edit it with your API keys:"
    print_info "  nano .env.production"
    print_info "Required: OPENAI_API_KEY"
    read -p "Press Enter after you've edited .env.production..."
else
    print_info ".env.production already exists"
fi

# Validate environment file
if ! grep -q "OPENAI_API_KEY=sk-" .env.production; then
    print_error "OPENAI_API_KEY not set in .env.production"
    print_info "Please edit the file: nano .env.production"
    exit 1
fi

print_status "Step 7: Creating log directories..."
sudo mkdir -p /var/log/resumecoach
sudo chown -R ubuntu:ubuntu /var/log/resumecoach
mkdir -p /run/resumecoach

print_status "Step 8: Setting up systemd service..."
sudo cp deployment/systemd-service.conf /etc/systemd/system/resumecoach-backend.service
sudo systemctl daemon-reload
sudo systemctl enable resumecoach-backend
sudo systemctl start resumecoach-backend

print_status "Step 9: Configuring Nginx..."
sudo cp deployment/nginx.conf /etc/nginx/sites-available/resumecoach
sudo ln -sf /etc/nginx/sites-available/resumecoach /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

print_status "Step 10: Testing backend health..."
sleep 5
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    print_status "Backend is running and healthy!"
else
    print_error "Backend health check failed. Check logs:"
    print_info "  sudo journalctl -u resumecoach-backend -n 50"
    exit 1
fi

print_status "Step 11: Setting up SSL (optional)..."
read -p "Do you want to set up SSL with Let's Encrypt? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter your domain name (e.g., api.resumecoach.com): " DOMAIN
    if [ -n "$DOMAIN" ]; then
        sudo certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email admin@resumecoach.com
        print_status "SSL configured for $DOMAIN"
    fi
fi

print_status "Step 12: Setting up CloudWatch monitoring (optional)..."
read -p "Do you want to install CloudWatch agent? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
    sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
    rm amazon-cloudwatch-agent.deb
    print_info "CloudWatch agent installed. Configure it with:"
    print_info "  sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard"
fi

echo ""
echo "=================================================="
print_status "Deployment completed successfully! 🎉"
echo "=================================================="
echo ""
echo "Service Status:"
sudo systemctl status resumecoach-backend --no-pager -l | grep -E "Active:|Main PID:"
echo ""
echo "Next Steps:"
echo "1. Test your API: curl http://$(curl -s ifconfig.me)/api/health"
echo "2. View logs: sudo journalctl -u resumecoach-backend -f"
echo "3. Monitor Nginx: sudo tail -f /var/log/nginx/access.log"
echo ""
echo "Management Commands:"
echo "  Start:   sudo systemctl start resumecoach-backend"
echo "  Stop:    sudo systemctl stop resumecoach-backend"
echo "  Restart: sudo systemctl restart resumecoach-backend"
echo "  Status:  sudo systemctl status resumecoach-backend"
echo "  Logs:    sudo journalctl -u resumecoach-backend -n 100"
echo ""
print_info "Don't forget to configure your Streamlit Cloud frontend with:"
print_info "  API_BASE_URL=http://$(curl -s ifconfig.me)"
echo ""
