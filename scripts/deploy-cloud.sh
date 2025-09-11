#!/bin/bash

# Cloud Deployment Script for Portfolio
# Supports DigitalOcean, AWS, and other cloud providers

set -e

echo "🌐 Portfolio Cloud Deployment Script"
echo "===================================="

# Configuration
DOMAIN=${1:-""}
PLATFORM=${2:-"digitalocean"}
DB_TYPE=${3:-"atlas"}

if [ -z "$DOMAIN" ]; then
    echo "❌ Usage: ./deploy-cloud.sh <domain> [platform] [db_type]"
    echo "   Example: ./deploy-cloud.sh albeejohn.com digitalocean atlas"
    echo "   Platform options: digitalocean, aws, railway"
    echo "   DB options: atlas, local"
    exit 1
fi

echo "📋 Configuration:"
echo "   Domain: $DOMAIN"
echo "   Platform: $PLATFORM"
echo "   Database: $DB_TYPE"
echo ""

# Check if environment files exist
if [ ! -f "backend/.env.production" ] || [ ! -f "frontend/.env.production" ]; then
    echo "❌ Production environment files not found!"
    echo "   Please run: ./scripts/setup-environment.sh $DOMAIN first"
    exit 1
fi

# Platform-specific deployment
case $PLATFORM in
    "digitalocean")
        echo "🌊 Deploying to DigitalOcean..."
        
        # Update environment with domain
        sed -i "s/yourdomain.com/$DOMAIN/g" backend/.env.production
        sed -i "s/yourdomain.com/$DOMAIN/g" frontend/.env.production
        
        # Copy environment files
        cp backend/.env.production backend/.env
        cp frontend/.env.production frontend/.env
        
        # Build and deploy
        docker-compose down || true
        docker-compose build --no-cache
        docker-compose up -d
        
        echo "⏳ Waiting for services to start..."
        sleep 30
        
        # Health check
        for i in {1..10}; do
            if curl -f "http://localhost/api/health" > /dev/null 2>&1; then
                echo "✅ Services are healthy!"
                break
            fi
            
            if [ $i -eq 10 ]; then
                echo "❌ Health check failed!"
                docker-compose logs --tail=20
                exit 1
            fi
            
            echo "⏳ Health check attempt $i, retrying..."
            sleep 10
        done
        
        ;;
        
    "aws")
        echo "☁️ Deploying to AWS..."
        echo "⚠️ Make sure you have AWS CLI configured!"
        
        # Check AWS CLI
        if ! command -v aws &> /dev/null; then
            echo "❌ AWS CLI not found! Please install and configure it first."
            exit 1
        fi
        
        # Update environment with domain
        sed -i "s/yourdomain.com/$DOMAIN/g" backend/.env.production
        sed -i "s/yourdomain.com/$DOMAIN/g" frontend/.env.production
        
        # Deploy using Docker
        cp backend/.env.production backend/.env
        cp frontend/.env.production frontend/.env
        
        docker-compose down || true
        docker-compose build --no-cache
        docker-compose up -d
        
        ;;
        
    "railway")
        echo "🚂 Deploying to Railway..."
        echo "ℹ️ Please configure environment variables in Railway dashboard:"
        echo ""
        echo "Backend Environment Variables:"
        cat backend/.env.production | grep -v "^#" | sed 's/^/  /'
        echo ""
        echo "Frontend Environment Variables:"
        cat frontend/.env.production | grep -v "^#" | sed 's/^/  /'
        echo ""
        echo "📋 Then push to GitHub and Railway will auto-deploy!"
        
        ;;
        
    *)
        echo "❌ Unsupported platform: $PLATFORM"
        echo "   Supported platforms: digitalocean, aws, railway"
        exit 1
        ;;
esac

# SSL Setup (if not Railway)
if [ "$PLATFORM" != "railway" ]; then
    echo ""
    echo "🔐 Setting up SSL certificate..."
    
    if command -v certbot &> /dev/null; then
        # Attempt automatic SSL setup
        certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "admin@$DOMAIN" || {
            echo "⚠️ Automatic SSL setup failed. Please run manually:"
            echo "   sudo certbot --nginx -d $DOMAIN"
        }
    else
        echo "⚠️ Certbot not found. Please install and run:"
        echo "   sudo apt install certbot python3-certbot-nginx"
        echo "   sudo certbot --nginx -d $DOMAIN"
    fi
fi

# Final verification
echo ""
echo "🔍 Final verification..."

# Check HTTP
if curl -s "http://$DOMAIN/api/health" | grep -q "healthy"; then
    echo "✅ HTTP endpoint working"
else
    echo "⚠️ HTTP endpoint not responding"
fi

# Check HTTPS (if SSL was set up)
if curl -s "https://$DOMAIN/api/health" | grep -q "healthy" 2>/dev/null; then
    echo "✅ HTTPS endpoint working"
else
    echo "⚠️ HTTPS endpoint not ready (SSL may need manual setup)"
fi

echo ""
echo "🎉 Deployment completed!"
echo ""
echo "📋 Your portfolio is now available at:"
echo "   HTTP:  http://$DOMAIN"
echo "   HTTPS: https://$DOMAIN (if SSL is configured)"
echo ""
echo "📊 Monitor your deployment:"
echo "   Health: https://$DOMAIN/api/health"
echo "   Detailed: https://$DOMAIN/api/health/detailed"
echo ""
echo "🛠️ Management commands:"
echo "   Status: docker-compose ps"
echo "   Logs: docker-compose logs -f"
echo "   Restart: docker-compose restart"
echo "   Monitor: ./scripts/monitor.sh"

# Create deployment record
cat > "deployment_$(date +%Y%m%d_%H%M%S).log" << EOF
Deployment completed at: $(date)
Domain: $DOMAIN
Platform: $PLATFORM
Database: $DB_TYPE
Services:
$(docker-compose ps)

Environment Variables Set:
Backend: $(wc -l < backend/.env) variables
Frontend: $(wc -l < frontend/.env) variables

Health Check:
$(curl -s "http://$DOMAIN/api/health" 2>/dev/null || echo "Not available")
EOF

echo "📝 Deployment log saved"