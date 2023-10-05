#!/usr/bin/env bash
# This script sets up web servers for web_static deployment

# Install Nginx if not already installed
if ! dpkg -l nginx | grep -q "ii"; then
    apt-get update
    apt-get -y install nginx
fi

# Create necessary directories
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

# Create a fake HTML file
echo "<html><head></head><body>Holberton School</body></html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
sed -i '/location \/hbnb_static {/a alias /data/web_static/current/;' $config_file

# Restart Nginx
service nginx restart

exit 0
