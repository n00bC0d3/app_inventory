#!/bin/bash
set -e

echo "🚀 Starting Inventory App Deployment..."

# ============================================
# 1. System Update
# ============================================
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# ============================================
# 2. Install Dependencies
# ============================================
echo "📦 Installing dependencies..."
sudo apt install -y python3-pip python3-venv python3-dev \
                    nginx git curl wget build-essential \
                    libpq-dev postgresql-client redis-tools

# ============================================
# 3. Create Application Directory
# ============================================
echo "📁 Creating application directory..."
sudo git clone https://github.com/n00bC0d3/app_inventory.git /var/www/inventory_app
#sudo mkdir -p /var/www/inventory_app
sudo chown -R $USER:$USER /var/www/inventory_app
cd /var/www/inventory_app

# ============================================
# 4. Upload Application Files
# ============================================
# echo "📄 Upload application files to /var/www/inventory_app"
# echo "   Required files: app.py, config.py, requirements.txt,"
# echo "   gunicorn.conf.py, templates/"
# echo "   Press Enter when files are uploaded..."
# read 

# ============================================
# 5. Create Virtual Environment
# ============================================
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ============================================
# 6. Configure Environment Variables
# ============================================
echo "⚙️  Creating .env file..."
cp .env.example .env

# ============================================
# 7. Initialize Database
# ============================================
echo "🗄️  Initializing database..."
python app.py

# ============================================
# 8. Configure Systemd Service
# ============================================
echo "⚙️  Creating systemd service..."
sudo bash -c 'cat > /etc/systemd/system/inventory_app.service << EOF
[Unit]
Description=Inventory App
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/var/www/inventory_app
Environment="PATH=/var/www/inventory_app/venv/bin"
ExecStart=/var/www/inventory_app/venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF'

# ============================================
# 9. Configure Nginx
# ============================================
echo "🌐 Configuring Nginx..."
sudo bash -c 'cat > /etc/nginx/sites-available/inventory_app << EOF
server {
    listen 80 default_server;
    server_name _ ;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF'

sudo ln -sf /etc/nginx/sites-available/inventory_app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

sudo nginx -t

# ============================================
# 10. Start Services
# ============================================
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable inventory_app.service
sudo systemctl start inventory_app.service
sudo systemctl restart nginx

# ============================================
# 11. Verification
# ============================================
echo "✅ Deployment Complete!"
echo ""
echo "📊 Service Status:"
sudo systemctl status inventory_app.service --no-pager
echo ""
echo "🌐 Nginx Status:"
sudo systemctl status nginx --no-pager
echo ""
echo "🔗 Access your application at:"
echo "   http://$(curl -s ifconfig.me)"
echo ""
echo "🔐 Default Login:"
echo "   Username: admin"
echo "   Password: password123"
echo ""
echo "⚠️  Change the default password immediately!"