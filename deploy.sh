#!/bin/bash

# Load environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ .env file not found!"
    exit 1
fi

NGINX_CONF_PATH="/etc/nginx/sites-available/$SERVICE_NAME"
NGINX_ENABLED_PATH="/etc/nginx/sites-enabled/$SERVICE_NAME"

# Clone or pull repo
if [ -d "$APP_DIR/.git" ]; then
    echo "🔄 Pulling latest code from 'production' branch..."
    cd "$APP_DIR"
    git fetch origin
    git checkout production
    git pull origin production
else
    echo "📥 Cloning repo and checking out 'production' branch..."
    git clone --branch production "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi

# Build frontend
echo "📦 Installing frontend dependencies and building Vue..."
cd vue || exit 1
yarn install --frozen-lockfile
yarn build
cd ..

# Build backend
echo "⚙️ Building Go backend..."
cd server || exit 1
go build -o ../syslabmgr
cd ..

# Set permissions
echo "🔐 Setting file permissions..."
sudo chown -R www-data:www-data "$APP_DIR"

# Nginx reverse proxy setup
echo "🌐 Setting up Nginx reverse proxy..."

sudo tee "$NGINX_CONF_PATH" > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_NAME;

    location / {
        proxy_pass http://localhost:$APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable site
if [ ! -L "$NGINX_ENABLED_PATH" ]; then
    sudo ln -s "$NGINX_CONF_PATH" "$NGINX_ENABLED_PATH"
fi

sudo nginx -t && sudo systemctl reload nginx


# 🔧 Create systemd service unit file
echo "🛠️ Generating systemd service: $SERVICE_NAME.service..."

sudo tee "/etc/systemd/system/$SERVICE_NAME.service" > /dev/null <<EOF
[Unit]
Description=SysLabMgr Service
After=network.target

[Service]
Type=simple
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/syslabmgr
Restart=on-failure
User=www-data
Group=www-data
Environment=PORT=$APP_PORT

[Install]
WantedBy=multi-user.target
EOF

# 🔄 Reload and enable the service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "✅ Deployment complete. Access it at: http://$SERVER_NAME"
