#!/bin/bash

# Production Setup Script for Portfolio Deployment
# This script prepares the server for production deployment

set -e

echo "🚀 Starting Production Setup..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (sudo ./setup-production.sh)"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
apt-get update && apt-get upgrade -y

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker $SUDO_USER
    rm get-docker.sh
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "🐳 Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Install essential tools
echo "🛠️ Installing essential tools..."
apt-get install -y curl wget git ufw htop nginx-extras

# Configure firewall
echo "🔒 Configuring firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Create application user
echo "👤 Setting up application user..."
if ! id "portfolio" &>/dev/null; then
    useradd -m -s /bin/bash portfolio
    usermod -aG docker portfolio
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p /var/www/portfolio
mkdir -p /var/log/portfolio
mkdir -p /var/backups/portfolio

# Set permissions
chown -R portfolio:portfolio /var/www/portfolio
chown -R portfolio:portfolio /var/log/portfolio
chown -R portfolio:portfolio /var/backups/portfolio

# Install SSL tool (Certbot)
echo "🔐 Installing SSL certificate tool..."
apt-get install -y snapd
snap install core; snap refresh core
snap install --classic certbot
ln -sf /snap/bin/certbot /usr/bin/certbot

# Create systemd service for automatic backups
echo "💾 Setting up backup service..."
cat > /etc/systemd/system/portfolio-backup.service << 'EOF'
[Unit]
Description=Portfolio Database Backup
Wants=portfolio-backup.timer

[Service]
Type=oneshot
User=portfolio
ExecStart=/var/www/portfolio/scripts/backup.sh
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

cat > /etc/systemd/system/portfolio-backup.timer << 'EOF'
[Unit]
Description=Run portfolio backup daily
Requires=portfolio-backup.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable portfolio-backup.timer

# Setup log rotation
echo "📋 Setting up log rotation..."
cat > /etc/logrotate.d/portfolio << 'EOF'
/var/log/portfolio/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 portfolio portfolio
    postrotate
        docker-compose -f /var/www/portfolio/docker-compose.yml restart portfolio > /dev/null 2>&1 || true
    endscript
}
EOF

# Create monitoring script
echo "📊 Setting up monitoring..."
cat > /usr/local/bin/portfolio-status << 'EOF'
#!/bin/bash
cd /var/www/portfolio
./scripts/monitor.sh
EOF
chmod +x /usr/local/bin/portfolio-status

# Setup fail2ban for additional security
echo "🛡️ Setting up fail2ban..."
apt-get install -y fail2ban

cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
backend = %(sshd_backend)s

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

[nginx-noscript]
enabled = true
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 6
EOF

systemctl enable fail2ban
systemctl start fail2ban

echo ""
echo "✅ Production setup completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Clone your portfolio repository to /var/www/portfolio"
echo "2. Configure environment variables"
echo "3. Run deployment script"
echo "4. Set up SSL certificate with: certbot --nginx -d yourdomain.com"
echo ""
echo "📊 Useful Commands:"
echo "- Monitor: portfolio-status"
echo "- Logs: tail -f /var/log/portfolio/*.log"
echo "- Service status: systemctl status portfolio-backup"
echo ""
echo "🔐 Security:"
echo "- Firewall is active with only necessary ports open"
echo "- Fail2ban is protecting against brute force attacks"
echo "- Log rotation is configured"
echo "- Daily backups are scheduled"