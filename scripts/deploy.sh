#!/bin/bash

# Portfolio Deployment Script
# This script handles deployment to production environment

set -e

echo "🚀 Starting Portfolio Deployment..."

# Configuration
ENVIRONMENT=${1:-production}
BUILD_TAG=${2:-$(date +%Y%m%d_%H%M%S)}
COMPOSE_FILE="docker-compose.yml"

if [ "$ENVIRONMENT" = "staging" ]; then
    COMPOSE_FILE="docker-compose.staging.yml"
fi

echo "📋 Environment: $ENVIRONMENT"
echo "🏷️  Build Tag: $BUILD_TAG"

# Pre-deployment checks
echo "🔍 Running pre-deployment checks..."

# Check if required files exist
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ $COMPOSE_FILE not found"
    exit 1
fi

if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found"
    exit 1
fi

# Check if environment variables are set
if [ "$ENVIRONMENT" = "production" ] && [ ! -f "backend/.env.production" ]; then
    echo "❌ Production environment file not found"
    exit 1
fi

echo "✅ Pre-deployment checks passed"

# Build and deploy
echo "🔨 Building application..."
docker-compose -f "$COMPOSE_FILE" build --no-cache

echo "🔄 Stopping existing services..."
docker-compose -f "$COMPOSE_FILE" down

echo "🗃️  Cleaning up unused images..."
docker image prune -f

echo "📦 Starting services..."
docker-compose -f "$COMPOSE_FILE" up -d

# Health check
echo "🏥 Waiting for services to be healthy..."
sleep 30

HEALTH_CHECK_URL="http://localhost/api/health"
if [ "$ENVIRONMENT" = "production" ]; then
    HEALTH_CHECK_URL="https://yourdomain.com/api/health"
fi

for i in {1..10}; do
    if curl -f "$HEALTH_CHECK_URL" > /dev/null 2>&1; then
        echo "✅ Health check passed"
        break
    fi
    
    if [ $i -eq 10 ]; then
        echo "❌ Health check failed after 10 attempts"
        echo "📋 Service status:"
        docker-compose -f "$COMPOSE_FILE" ps
        echo "📋 Application logs:"
        docker-compose -f "$COMPOSE_FILE" logs --tail=20
        exit 1
    fi
    
    echo "⏳ Health check attempt $i failed, retrying in 10s..."
    sleep 10
done

# Post-deployment tasks
echo "🔧 Running post-deployment tasks..."

# Seed database if needed
echo "🌱 Seeding database..."
docker-compose -f "$COMPOSE_FILE" exec portfolio python /app/backend/seed_data.py || echo "⚠️  Database seeding skipped (data may already exist)"

# Create deployment record
echo "📝 Creating deployment record..."
cat > "deployment_$BUILD_TAG.log" << EOF
Deployment completed at: $(date)
Environment: $ENVIRONMENT
Build Tag: $BUILD_TAG
Deployed by: $(whoami)
Git Commit: $(git rev-parse HEAD 2>/dev/null || echo "N/A")
Services:
$(docker-compose -f "$COMPOSE_FILE" ps)
EOF

echo "🎉 Deployment completed successfully!"
echo "🌐 Application URL: $HEALTH_CHECK_URL"
echo "📊 Monitor status: docker-compose -f $COMPOSE_FILE ps"
echo "📋 View logs: docker-compose -f $COMPOSE_FILE logs -f"

# Optional: Send notification (Slack, Discord, etc.)
# curl -X POST -H 'Content-type: application/json' \
#   --data '{"text":"Portfolio deployment completed successfully!"}' \
#   YOUR_WEBHOOK_URL