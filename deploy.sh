#!/bin/bash

# GitHub Pages + Railway Quick Deploy Script
# Run this script to prepare your portfolio for deployment

set -e

echo "🚀 Portfolio Deployment Preparation"
echo "=================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is configured
echo -e "${BLUE}Checking Git configuration...${NC}"
if ! git config user.name > /dev/null; then
    echo -e "${RED}❌ Git user not configured${NC}"
    read -p "Enter your Git username: " git_username
    git config --global user.name "$git_username"
fi

if ! git config user.email > /dev/null; then
    echo -e "${RED}❌ Git email not configured${NC}"
    read -p "Enter your Git email: " git_email
    git config --global user.email "$git_email"
fi

echo -e "${GREEN}✅ Git configured${NC}"

# Initialize Git repository if not exists
if [ ! -d ".git" ]; then
    echo -e "${BLUE}Initializing Git repository...${NC}"
    git init
    git add .
    git commit -m "Initial commit: Portfolio deployment ready"
    echo -e "${GREEN}✅ Git repository initialized${NC}"
else
    echo -e "${GREEN}✅ Git repository exists${NC}"
fi

# Add GitHub remote
echo -e "${BLUE}Setting up GitHub remote...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/AlbeeJohn/portfolio.git
echo -e "${GREEN}✅ GitHub remote configured${NC}"

# Install frontend dependencies
echo -e "${BLUE}Installing frontend dependencies...${NC}"
cd frontend
if command -v yarn &> /dev/null; then
    yarn install
else
    npm install
fi
cd ..
echo -e "${GREEN}✅ Frontend dependencies installed${NC}"

# Test frontend build
echo -e "${BLUE}Testing frontend build...${NC}"
cd frontend
if command -v yarn &> /dev/null; then
    REACT_APP_BACKEND_URL=https://portfolio-backend-production-albeejohn.up.railway.app yarn run build
else
    REACT_APP_BACKEND_URL=https://portfolio-backend-production-albeejohn.up.railway.app npm run build
fi
cd ..
echo -e "${GREEN}✅ Frontend build successful${NC}"

# Install backend dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
cd backend
python -m pip install -r requirements.txt
cd ..
echo -e "${GREEN}✅ Backend dependencies installed${NC}"

echo ""
echo "🎉 DEPLOYMENT PREPARATION COMPLETE!"
echo "=================================="
echo ""
echo "📋 Next Steps:"
echo "1. Create MongoDB Atlas account: https://www.mongodb.com/atlas/database"
echo "2. Create Railway account: https://railway.app"
echo "3. Push to GitHub: git push -u origin main"
echo "4. Enable GitHub Pages in repository settings"
echo "5. Deploy backend to Railway"
echo ""
echo "📖 Full instructions: See GITHUB_RAILWAY_DEPLOYMENT.md"
echo ""
echo "🌐 Your URLs after deployment:"
echo "   Frontend: https://albeejohn.github.io/portfolio"
echo "   Backend:  https://portfolio-backend-production-albeejohn.up.railway.app"
echo ""
echo -e "${GREEN}Ready to deploy! 🚀${NC}"