# 🚀 AWS Free Tier Deployment Guide for Portfolio

## 🎯 **DEPLOYMENT PLAN**
- **Platform**: AWS Free Tier (12 months free)
- **Budget**: Free (with minimal domain cost)
- **Domain**: New domain required

---

## 💰 **COST BREAKDOWN**

### **Free Components (AWS Free Tier):**
- ✅ **EC2 t2.micro**: 750 hours/month (always free)
- ✅ **EBS Storage**: 30GB (free tier)
- ✅ **SSL Certificate**: Free with AWS Certificate Manager
- ✅ **CloudWatch**: Basic monitoring (free tier)
- ✅ **Data Transfer**: 15GB out/month (free tier)

### **Domain Name Options:**
1. **Freenom** (.tk, .ml, .ga) - **FREE** but limited features
2. **Namecheap** (.com) - **$8.98/year** (recommended)
3. **AWS Route 53** (.com) - **$12/year + $0.50/month DNS**
4. **Cloudflare** (.com) - **$9.15/year**

### **Total Monthly Cost:**
- **Option 1**: $0/month + $0/year domain = **FREE**
- **Option 2**: $0/month + $9/year domain = **$0.75/month**

---

## 🛠️ **AWS DEPLOYMENT STEPS**

### **STEP 1: AWS Account Setup**
1. **Create AWS Account**: https://aws.amazon.com/free/
2. **Verify payment method** (won't charge for free tier)
3. **Enable MFA** for security

### **STEP 2: Domain Setup**
Choose your preferred option:

#### **Option A: Free Domain (Freenom)**
1. Go to https://freenom.com
2. Search for available domain (yourname.tk, yourname.ml)
3. Register for 12 months free
4. Note: Limited features, may have ads

#### **Option B: Paid Domain (Recommended)**
1. **Namecheap**: Go to https://namecheap.com
2. **Search** for your preferred domain
3. **Purchase** (.com ~$9/year)
4. **Better** for professional appearance

### **STEP 3: Launch EC2 Instance**
```bash
# We'll do this through AWS Console, but here's what we'll set up:
# - Instance: t2.micro (free tier)
# - OS: Ubuntu 22.04 LTS
# - Storage: 30GB EBS (free tier)
# - Security Group: HTTP (80), HTTPS (443), SSH (22)
```

---

## 📋 **DETAILED DEPLOYMENT PROCESS**

I'll guide you through each step. Let's start:

### **🎯 IMMEDIATE ACTION ITEMS:**

1. **AWS Account**:
   - Do you have an AWS account? (If not, create at aws.amazon.com/free)
   - Have you verified your payment method?

2. **Domain Preference**:
   - **Free domain** (yourname.tk) - Limited but costs nothing
   - **Paid domain** (yourname.com) - Professional, ~$9/year
   
3. **Preferred Domain Name**:
   - What domain name do you want? (e.g., albeejohn.com, john-portfolio.com)

---

## 🚀 **QUICK START COMMANDS** (Ready to use)

Once we have your AWS instance and domain ready, deployment is simple:

```bash
# 1. Connect to your EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Setup production environment
wget https://raw.githubusercontent.com/your-repo/Portfolio/main/scripts/setup-production.sh
chmod +x setup-production.sh
sudo ./setup-production.sh

# 3. Clone and deploy
git clone https://github.com/your-repo/Portfolio.git
cd Portfolio
./scripts/setup-environment.sh your-domain.com
./scripts/deploy-cloud.sh your-domain.com aws
```

---

## 🔧 **AUTOMATION SCRIPT** (Ready for AWS)