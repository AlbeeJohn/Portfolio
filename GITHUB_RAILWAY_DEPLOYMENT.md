# 🚀 GitHub Pages + Railway Deployment Guide

## ✅ **DEPLOYMENT ARCHITECTURE**
- **Frontend**: GitHub Pages (`albeejohn.github.io`)
- **Backend**: Railway (`portfolio-backend-production-albeejohn.up.railway.app`)
- **Database**: MongoDB Atlas (Free Tier)
- **Total Cost**: **FREE** 🎉

---

## 🎯 **STEP-BY-STEP DEPLOYMENT**

### **STEP 1: Setup MongoDB Atlas (Database)**
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas/database)
2. Create free account
3. Create a **FREE cluster**
4. Create database user: `portfolio_user`
5. **Whitelist all IPs**: `0.0.0.0/0` (for Railway access)
6. **Copy connection string**: 
   ```
   mongodb+srv://portfolio_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/portfolio?retryWrites=true&w=majority
   ```

### **STEP 2: Deploy Backend to Railway**
1. Go to [Railway.app](https://railway.app)
2. **Sign up** with GitHub account
3. Click "**Start a New Project**"
4. Select "**Deploy from GitHub repo**"
5. Connect your GitHub account
6. Select the portfolio repository
7. Choose "**backend**" folder as root directory

**Set Environment Variables in Railway:**
```bash
MONGO_URL=mongodb+srv://portfolio_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/portfolio
JWT_SECRET=your-super-secret-jwt-key-min-32-chars
SECRET_KEY=your-super-secret-key-min-32-chars
CORS_ORIGINS=https://albeejohn.github.io,https://www.albeejohn.github.io
ENVIRONMENT=production
PORT=8000
DATABASE_NAME=portfolio
```

8. Click "**Deploy**"
9. **Copy your Railway URL**: `https://portfolio-backend-production-albeejohn.up.railway.app`

### **STEP 3: Deploy Frontend to GitHub Pages**
1. **Push code to GitHub**:
   ```bash
   # In your local repository
   git add .
   git commit -m "Add GitHub Pages + Railway deployment"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your GitHub repository
   - Settings → Pages
   - Source: "**GitHub Actions**"

3. **GitHub Actions will auto-deploy**:
   - Frontend builds automatically
   - Deployed to: `https://albeejohn.github.io/portfolio`

### **STEP 4: Verification**
1. **Check Backend**: Visit your Railway URL + `/api/health`
   ```
   https://portfolio-backend-production-albeejohn.up.railway.app/api/health
   ```

2. **Check Frontend**: Visit your GitHub Pages URL
   ```
   https://albeejohn.github.io/portfolio
   ```

3. **Test Contact Form**: Fill and submit the form

---

## 🔧 **CONFIGURATION DETAILS**

### **Automatic Deployments**
- ✅ **Frontend**: Auto-deploys when you push to `frontend/` folder
- ✅ **Backend**: Auto-deploys when you push to `backend/` folder
- ✅ **Both**: Use GitHub Actions workflows

### **URLs After Deployment**
```bash
Frontend:  https://albeejohn.github.io/portfolio
Backend:   https://portfolio-backend-production-albeejohn.up.railway.app
API:       https://portfolio-backend-production-albeejohn.up.railway.app/api
Health:    https://portfolio-backend-production-albeejohn.up.railway.app/api/health
```

---

## 💡 **IMPORTANT NOTES**

### **Domain Configuration**
- GitHub Pages URL will be: `albeejohn.github.io/portfolio`
- Repository name should be `portfolio` for this URL
- Or rename repo to `albeejohn.github.io` for root domain

### **Secret Keys Generation**
Generate secure secrets for production:
```bash
# JWT Secret (min 32 characters)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Secret Key (min 32 characters)  
python -c "import secrets; print(secrets.token_hex(32))"
```

### **CORS Configuration**
Backend automatically allows:
- `https://albeejohn.github.io`
- `https://www.albeejohn.github.io`
- `http://localhost:3000` (development)

---

## 🚀 **DEPLOYMENT CHECKLIST**

### **Before Going Live**
- [ ] MongoDB Atlas cluster created and configured
- [ ] Database user created with password
- [ ] Railway backend deployed with all environment variables
- [ ] GitHub repository pushed with all files
- [ ] GitHub Pages enabled in repository settings
- [ ] Backend health check working
- [ ] Frontend loading correctly

### **After Deployment**
- [ ] Test contact form submission
- [ ] Check all navigation links
- [ ] Verify responsive design on mobile
- [ ] Test loading speed
- [ ] Check browser console for errors

---

## 🎯 **QUICK DEPLOYMENT COMMANDS**

```bash
# 1. Clone to GitHub
git remote add origin https://github.com/AlbeeJohn/portfolio.git
git branch -M main
git push -u origin main

# 2. Local development (optional)
cd frontend && yarn install && yarn start
cd backend && pip install -r requirements.txt && python server.py

# 3. Check deployments
curl https://portfolio-backend-production-albeejohn.up.railway.app/api/health
```

---

## 📊 **COST BREAKDOWN**
- **MongoDB Atlas**: $0/month (512MB free tier)
- **Railway**: $0/month (500 hours free tier)  
- **GitHub Pages**: $0/month (unlimited for public repos)
- **Domain**: $0 (using github.io subdomain)
- **SSL**: $0 (automatic HTTPS)
- **Total**: **$0/month** 🎉

---

## 🔄 **MAKING UPDATES**

### **Frontend Changes**
```bash
# Make changes to frontend code
git add frontend/
git commit -m "Update frontend"
git push origin main
# Auto-deploys via GitHub Actions
```

### **Backend Changes**
```bash
# Make changes to backend code
git add backend/
git commit -m "Update backend API"  
git push origin main
# Auto-deploys via GitHub Actions to Railway
```

---

## 🆘 **TROUBLESHOOTING**

### **Common Issues**
1. **Backend not accessible**: Check Railway logs and environment variables
2. **CORS errors**: Verify CORS_ORIGINS includes your GitHub Pages URL
3. **Database connection**: Verify MongoDB Atlas IP whitelist (0.0.0.0/0)
4. **GitHub Pages not updating**: Check Actions tab for build errors

### **Health Check URLs**
- Backend: `https://your-railway-url/api/health`
- Portfolio Data: `https://your-railway-url/api/portfolio`
- Frontend: `https://albeejohn.github.io/portfolio`

---

**🎉 Your portfolio will be live at: `https://albeejohn.github.io/portfolio`**