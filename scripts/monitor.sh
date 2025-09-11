#!/bin/bash

# System Monitoring Script
echo "📊 Portfolio System Status"
echo "=========================="

# Docker services status
echo "🐳 Docker Services:"
docker-compose ps

echo ""

# System resources
echo "💻 System Resources:"
echo "CPU Usage: $(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')"
echo "Memory Usage: $(free | grep Mem | awk '{printf "%.2f%%", $3/$2 * 100.0}')"
echo "Disk Usage: $(df -h / | awk 'NR==2{printf "%s", $5}')"

echo ""

# Application health
echo "🏥 Health Checks:"
HEALTH_URL="http://localhost/api/health"
if curl -f "$HEALTH_URL" > /dev/null 2>&1; then
    echo "✅ Application: Healthy"
else
    echo "❌ Application: Unhealthy"
fi

# Database health
if docker exec portfolio_mongo_1 mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
    echo "✅ Database: Connected"
else
    echo "❌ Database: Disconnected"
fi

echo ""

# Recent logs (last 10 lines)
echo "📋 Recent Logs:"
docker-compose logs --tail=10 --timestamps

echo ""

# Performance metrics
echo "⚡ Performance:"
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' "$HEALTH_URL" 2>/dev/null || echo "N/A")
echo "API Response Time: ${RESPONSE_TIME}s"

# Database stats
DB_STATS=$(docker exec portfolio_mongo_1 mongosh portfolio_db --eval "
  db.portfolio.countDocuments()
" --quiet 2>/dev/null || echo "N/A")
echo "Portfolio Records: $DB_STATS"

CONTACT_STATS=$(docker exec portfolio_mongo_1 mongosh portfolio_db --eval "
  db.contact_messages.countDocuments()
" --quiet 2>/dev/null || echo "N/A")
echo "Contact Messages: $CONTACT_STATS"