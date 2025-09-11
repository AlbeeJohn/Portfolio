#!/bin/bash

# Environment Setup Script for Production Deployment
# This script helps configure all necessary environment variables

set -e

echo "⚙️ Portfolio Environment Setup"
echo "============================="

DOMAIN=${1:-""}

if [ -z "$DOMAIN" ]; then
    echo "❌ Usage: ./setup-environment.sh <domain>"
    echo "   Example: ./setup-environment.sh albeejohn.com"
    exit 1
fi

echo "🌐 Setting up environment for domain: $DOMAIN"
echo ""

# Function to generate random password
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-32
}

# Function to generate JWT secret
generate_jwt_secret() {
    openssl rand -base64 64 | tr -d "=+/" | cut -c1-64
}

echo "🔑 Generating secure secrets..."
SECRET_KEY=$(generate_password)
JWT_SECRET=$(generate_jwt_secret)

echo "✅ Secrets generated"
echo ""

# Get MongoDB connection details
echo "📊 Database Configuration"
echo "========================"
echo ""
echo "Choose database option:"
echo "1. MongoDB Atlas (Free tier available, recommended)"
echo "2. Local MongoDB (for testing)"
echo ""
read -p "Select option (1-2): " DB_CHOICE

case $DB_CHOICE in
    1)
        echo ""
        echo "📋 MongoDB Atlas Setup Instructions:"
        echo "1. Go to https://www.mongodb.com/cloud/atlas"
        echo "2. Create free account and cluster"
        echo "3. Create database user"
        echo "4. Get connection string"
        echo ""
        read -p "Enter MongoDB Atlas connection string: " MONGO_URL
        DB_NAME="portfolio_db"
        ;;
    2)
        MONGO_URL="mongodb://mongo:27017"
        DB_NAME="portfolio_db"
        echo "✅ Using local MongoDB"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""

# Email configuration
echo "📧 Email Configuration"
echo "====================="
echo ""
echo "Email service for contact form (optional):"
echo "1. Gmail SMTP (free)"
echo "2. SendGrid (free tier)"
echo "3. Skip email setup"
echo ""
read -p "Select option (1-3): " EMAIL_CHOICE

case $EMAIL_CHOICE in
    1)
        echo ""
        echo "📋 Gmail SMTP Setup:"
        echo "1. Enable 2-factor authentication in Gmail"
        echo "2. Generate App Password: https://support.google.com/accounts/answer/185833"
        echo ""
        read -p "Enter Gmail address: " SMTP_USER
        read -p "Enter App Password: " SMTP_PASS
        SMTP_HOST="smtp.gmail.com"
        SMTP_PORT="587"
        ;;
    2)
        echo ""
        echo "📋 SendGrid Setup:"
        echo "1. Create account at https://sendgrid.com"
        echo "2. Generate API key"
        echo ""
        read -p "Enter SendGrid API key: " SENDGRID_KEY
        SMTP_USER="apikey"
        SMTP_PASS="$SENDGRID_KEY"
        SMTP_HOST="smtp.sendgrid.net"
        SMTP_PORT="587"
        ;;
    3)
        echo "⚠️ Skipping email configuration"
        SMTP_HOST="smtp.gmail.com"
        SMTP_PORT="587"
        SMTP_USER="your-email@gmail.com"
        SMTP_PASS="your-app-password"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""

# Create backend environment file
echo "📝 Creating backend environment file..."
cat > backend/.env.production << EOF
# Production Environment Variables for Portfolio Backend
# Generated on $(date)

# Database Configuration
MONGO_URL=$MONGO_URL
DB_NAME=$DB_NAME

# Security
SECRET_KEY=$SECRET_KEY
JWT_SECRET=$JWT_SECRET

# CORS Configuration
CORS_ORIGINS=https://$DOMAIN,https://www.$DOMAIN,http://$DOMAIN,http://www.$DOMAIN

# Email Configuration
SMTP_HOST=$SMTP_HOST
SMTP_PORT=$SMTP_PORT
SMTP_USER=$SMTP_USER
SMTP_PASS=$SMTP_PASS

# Performance
CACHE_TTL=1800
RATE_LIMIT_REQUESTS_PER_MINUTE=100
CONTACT_RATE_LIMIT_PER_MINUTE=5

# Logging
LOG_LEVEL=INFO

# Optional: Error Tracking (uncomment and configure if needed)
# SENTRY_DSN=your-sentry-dsn-for-backend-error-tracking

# Optional: Redis (uncomment if using Redis for caching)
# REDIS_URL=redis://redis:6379
EOF

# Create frontend environment file
echo "📝 Creating frontend environment file..."
cat > frontend/.env.production << EOF
# Production Environment Variables for Portfolio Frontend
# Generated on $(date)

# API Configuration
REACT_APP_BACKEND_URL=https://$DOMAIN
REACT_APP_ENVIRONMENT=production
REACT_APP_VERSION=1.0.0

# SEO Configuration
REACT_APP_SITE_URL=https://$DOMAIN
REACT_APP_SITE_NAME=Albee John - Data Analyst Portfolio

# Features
REACT_APP_ENABLE_SERVICE_WORKER=true
REACT_APP_ENABLE_PERFORMANCE_MONITOR=false
REACT_APP_ENABLE_ERROR_TRACKING=true

# Optional: Analytics (uncomment and configure if needed)
# REACT_APP_GOOGLE_ANALYTICS_ID=your-ga-tracking-id
# REACT_APP_HOTJAR_ID=your-hotjar-id

# Optional: Error Tracking (uncomment and configure if needed)
# REACT_APP_SENTRY_DSN=your-frontend-sentry-dsn
EOF

echo "✅ Environment files created!"
echo ""

# Create deployment summary
cat > DEPLOYMENT_CONFIG.md << EOF
# Deployment Configuration Summary

## Generated: $(date)
## Domain: $DOMAIN

### 🔑 Security
- Secret Key: Generated (32 characters)
- JWT Secret: Generated (64 characters)

### 📊 Database
- Type: $([ "$DB_CHOICE" = "1" ] && echo "MongoDB Atlas" || echo "Local MongoDB")
- Connection: $MONGO_URL
- Database Name: $DB_NAME

### 📧 Email
- Service: $([ "$EMAIL_CHOICE" = "1" ] && echo "Gmail SMTP" || [ "$EMAIL_CHOICE" = "2" ] && echo "SendGrid" || echo "Not configured")
- Host: $SMTP_HOST
- Port: $SMTP_PORT

### 📁 Files Created
- backend/.env.production
- frontend/.env.production

### 📋 Next Steps
1. Review the generated environment files
2. Run deployment: ./scripts/deploy-cloud.sh $DOMAIN
3. Set up SSL certificate
4. Test the deployment

### 🔒 Security Notes
- Keep environment files secure and never commit to git
- Regularly rotate secrets
- Monitor logs for suspicious activity
- Set up backups

### 📊 Monitoring URLs (after deployment)
- Health Check: https://$DOMAIN/api/health
- Detailed Health: https://$DOMAIN/api/health/detailed
- API Documentation: https://$DOMAIN/api/docs
EOF

echo "📋 Configuration Summary:"
echo ""
echo "✅ Backend environment: backend/.env.production"
echo "✅ Frontend environment: frontend/.env.production"  
echo "✅ Configuration summary: DEPLOYMENT_CONFIG.md"
echo ""
echo "🚀 Ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Review the generated files"
echo "2. Run: ./scripts/deploy-cloud.sh $DOMAIN"
echo ""
echo "⚠️ Important: Keep the .env.production files secure!"
echo "   - Never commit them to git"
echo "   - Store backup copies safely"
echo "   - Rotate secrets regularly"