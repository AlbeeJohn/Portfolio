#!/bin/bash

# AWS Free Tier Portfolio Deployment Script
# This script automates the entire AWS deployment process

set -e

echo "🚀 AWS Free Tier Portfolio Deployment"
echo "====================================="

# Configuration
REGION=${1:-"us-east-1"}
INSTANCE_TYPE="t2.micro"
DOMAIN=${2:-""}

if [ -z "$DOMAIN" ]; then
    echo "❌ Usage: ./deploy-aws-free.sh <region> <domain>"
    echo "   Example: ./deploy-aws-free.sh us-east-1 albeejohn.com"
    echo ""
    echo "📋 Available regions for free tier:"
    echo "   - us-east-1 (Virginia)"
    echo "   - us-west-2 (Oregon)"
    echo "   - eu-west-1 (Ireland)"
    echo "   - ap-southeast-1 (Singapore)"
    exit 1
fi

echo "📋 Deployment Configuration:"
echo "   Region: $REGION"
echo "   Instance: $INSTANCE_TYPE (Free Tier)"
echo "   Domain: $DOMAIN"
echo ""

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found!"
    echo "   Install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS credentials not configured!"
    echo "   Run: aws configure"
    exit 1
fi

echo "✅ AWS CLI configured"

# Create or get VPC
echo "🌐 Setting up VPC..."
VPC_ID=$(aws ec2 describe-vpcs --region $REGION --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text)

if [ "$VPC_ID" = "None" ]; then
    echo "❌ No default VPC found. Creating one..."
    aws ec2 create-default-vpc --region $REGION
    VPC_ID=$(aws ec2 describe-vpcs --region $REGION --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text)
fi

echo "✅ Using VPC: $VPC_ID"

# Create Security Group
echo "🔒 Creating security group..."
SG_ID=$(aws ec2 create-security-group \
    --region $REGION \
    --group-name portfolio-sg-$(date +%s) \
    --description "Portfolio security group" \
    --vpc-id $VPC_ID \
    --query 'GroupId' --output text 2>/dev/null || \
    aws ec2 describe-security-groups \
    --region $REGION \
    --filters "Name=group-name,Values=portfolio-sg*" \
    --query 'SecurityGroups[0].GroupId' --output text)

# Add security group rules
echo "🔐 Configuring security rules..."
aws ec2 authorize-security-group-ingress \
    --region $REGION \
    --group-id $SG_ID \
    --protocol tcp --port 22 --cidr 0.0.0.0/0 > /dev/null 2>&1 || echo "SSH rule exists"

aws ec2 authorize-security-group-ingress \
    --region $REGION \
    --group-id $SG_ID \
    --protocol tcp --port 80 --cidr 0.0.0.0/0 > /dev/null 2>&1 || echo "HTTP rule exists"

aws ec2 authorize-security-group-ingress \
    --region $REGION \
    --group-id $SG_ID \
    --protocol tcp --port 443 --cidr 0.0.0.0/0 > /dev/null 2>&1 || echo "HTTPS rule exists"

echo "✅ Security group configured: $SG_ID"

# Create or get key pair
echo "🔑 Setting up SSH key..."
KEY_NAME="portfolio-key-$(date +%s)"
aws ec2 create-key-pair \
    --region $REGION \
    --key-name $KEY_NAME \
    --query 'KeyMaterial' \
    --output text > $KEY_NAME.pem

chmod 400 $KEY_NAME.pem
echo "✅ SSH key created: $KEY_NAME.pem"

# Get latest Ubuntu AMI
echo "💿 Finding Ubuntu AMI..."
AMI_ID=$(aws ec2 describe-images \
    --region $REGION \
    --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    --query 'Images|sort_by(@, &CreationDate)[-1].ImageId' \
    --output text)

echo "✅ Using Ubuntu AMI: $AMI_ID"

# Launch EC2 instance
echo "🚀 Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances \
    --region $REGION \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_NAME \
    --security-group-ids $SG_ID \
    --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=30,VolumeType=gp2}' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=Portfolio-Server}]' \
    --user-data file://cloud-init.yml \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "✅ Instance launched: $INSTANCE_ID"

# Wait for instance to be running
echo "⏳ Waiting for instance to start..."
aws ec2 wait instance-running --region $REGION --instance-ids $INSTANCE_ID

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
    --region $REGION \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "✅ Instance running at: $PUBLIC_IP"

# Create cloud-init file for automatic setup
cat > cloud-init.yml << 'EOF'
#cloud-config
package_update: true
package_upgrade: true

packages:
  - docker.io
  - docker-compose
  - nginx
  - certbot
  - python3-certbot-nginx
  - git
  - curl
  - htop
  - ufw

users:
  - name: portfolio
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: docker
    shell: /bin/bash

runcmd:
  - systemctl enable docker
  - systemctl start docker
  - usermod -aG docker ubuntu
  - ufw --force enable
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow ssh
  - ufw allow 80/tcp
  - ufw allow 443/tcp
  - mkdir -p /var/www/portfolio
  - chown -R ubuntu:ubuntu /var/www/portfolio
EOF

# Wait for instance to be fully initialized
echo "⏳ Waiting for instance initialization (this may take 3-5 minutes)..."
sleep 180

# Test SSH connection
echo "🔗 Testing SSH connection..."
for i in {1..5}; do
    if ssh -o StrictHostKeyChecking=no -i $KEY_NAME.pem ubuntu@$PUBLIC_IP "echo 'SSH connection successful'" > /dev/null 2>&1; then
        echo "✅ SSH connection established"
        break
    fi
    
    if [ $i -eq 5 ]; then
        echo "❌ SSH connection failed after 5 attempts"
        echo "   Please wait a few more minutes and try manually:"
        echo "   ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP"
        exit 1
    fi
    
    echo "   Attempt $i failed, retrying in 30 seconds..."
    sleep 30
done

# Deploy application
echo "📦 Deploying portfolio application..."
ssh -o StrictHostKeyChecking=no -i $KEY_NAME.pem ubuntu@$PUBLIC_IP << 'ENDSSH'
    # Clone repository (you'll need to update this with your repo URL)
    cd /var/www/portfolio
    
    # For now, create a simple test
    echo "Portfolio deployment successful!" > index.html
    
    # Start simple nginx server
    sudo systemctl enable nginx
    sudo systemctl start nginx
    
    # Create basic nginx config
    sudo tee /etc/nginx/sites-available/portfolio << 'EOF'
server {
    listen 80;
    server_name _;
    root /var/www/portfolio;
    index index.html;
    
    location / {
        try_files $uri $uri/ =404;
    }
    
    location /api/health {
        return 200 '{"status":"healthy","service":"portfolio"}';
        add_header Content-Type application/json;
    }
}
EOF
    
    sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/default
    sudo systemctl reload nginx
ENDSSH

echo "✅ Basic deployment completed"

# Create Route 53 record (if using AWS domain)
echo "🌐 DNS Configuration needed..."
echo ""

# Summary
echo "🎉 AWS DEPLOYMENT COMPLETED!"
echo "=============================="
echo ""
echo "📋 Instance Details:"
echo "   Instance ID: $INSTANCE_ID"
echo "   Public IP: $PUBLIC_IP"
echo "   SSH Key: $KEY_NAME.pem"
echo "   Region: $REGION"
echo ""
echo "🔗 Access Methods:"
echo "   SSH: ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP"
echo "   HTTP: http://$PUBLIC_IP"
echo "   Health: http://$PUBLIC_IP/api/health"
echo ""
echo "📋 Next Steps:"
echo "1. Configure DNS to point $DOMAIN to $PUBLIC_IP"
echo "2. Set up SSL: ssh to instance and run 'sudo certbot --nginx -d $DOMAIN'"
echo "3. Deploy full portfolio: scp your code and run deployment scripts"
echo ""
echo "💰 Cost Monitoring:"
echo "   - This instance is FREE for 750 hours/month (first 12 months)"
echo "   - Monitor usage at: https://console.aws.amazon.com/billing/"
echo ""
echo "🔒 Security:"
echo "   - Keep your SSH key ($KEY_NAME.pem) secure"
echo "   - Change default SSH port if needed"
echo "   - Regularly update the system"
echo ""

# Save deployment info
cat > aws-deployment-info.txt << EOF
AWS Portfolio Deployment - $(date)
====================================

Instance ID: $INSTANCE_ID  
Public IP: $PUBLIC_IP
SSH Key: $KEY_NAME.pem
Region: $REGION
Security Group: $SG_ID
Domain: $DOMAIN

SSH Command:
ssh -i $KEY_NAME.pem ubuntu@$PUBLIC_IP

URLs:
- HTTP: http://$PUBLIC_IP
- HTTPS: https://$DOMAIN (after SSL setup)
- Health: http://$PUBLIC_IP/api/health

Estimated Monthly Cost: FREE (AWS Free Tier)
Free Tier Expires: $(date -d "+12 months" +"%Y-%m-%d")
EOF

echo "📝 Deployment info saved to: aws-deployment-info.txt"