# 🚀 Quick Start - Deploy Your Portfolio in 10 Minutes

## **TL;DR - Super Simple Steps**

### **1. Setup Free Database (2 minutes)**
- Go to [MongoDB Atlas](https://www.mongodb.com/atlas/database)
- Create free account → Create cluster → Create user → Copy connection string

### **2. Deploy Backend (3 minutes)**  
- Go to [Railway.app](https://railway.app) → Sign up with GitHub
- Create new project → Deploy from GitHub → Select this repository
- Set environment variables → Deploy

### **3. Deploy Frontend (2 minutes)**
- Push code to GitHub: `git push origin main`
- GitHub repository → Settings → Pages → Source: "GitHub Actions"

### **4. Done! (3 minutes)**
- Visit: `https://albeejohn.github.io/portfolio` 
- Test contact form

---

## **Environment Variables for Railway**

Copy these to Railway dashboard:

```bash
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/portfolio
JWT_SECRET=your-32-char-secret-key-here
SECRET_KEY=your-32-char-secret-key-here  
CORS_ORIGINS=https://albeejohn.github.io,https://www.albeejohn.github.io
ENVIRONMENT=production
PORT=8000
```

**Generate secrets:**
```bash
python -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
```

---

## **Final URLs**
- **Portfolio**: `https://albeejohn.github.io/portfolio`
- **API Health**: `https://your-railway-url/api/health`

**Total Time**: ~10 minutes | **Total Cost**: $0/month

📖 **Full Guide**: See `GITHUB_RAILWAY_DEPLOYMENT.md` for detailed instructions.