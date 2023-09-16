#!/usr/bin/env bash
# a Bash script that sets up your web servers for the deployment of web_static.

# Installing Nginx and configuring firewall
if ! command -v nginx; then
    sudo apt-get update &>/dev/null
    echo "Installing Nginx"
    sudo apt-get -y install nginx &>/dev/null
    sudo uwf allow 'Nginx HTTP' &>/dev/null
fi

# configure the Nginx config file to deploy static files
dir_1="/data/web_static/releases/test/"
symlink="/data/web_static/current"
dir_2="/data/web_static/shared/"

if ! [ -d "$dir_1" ]; then
    sudo mkdir -p "$dir_1"
    sudo sh -c 'echo "<html><head></head><body>Holberton School</body></html>" > /data/web_static/releases/test/index.html'
fi

if ! [ -d "$dir_2" ]; then
        sudo mkdir -p "$dir_2"
fi

if [ -e "$symlink" ]; then
    sudo rm -rf "$symlink"
    sudo ln -s "$dir_1" "$symlink"
else
    sudo ln -s "$dir_1" "$symlink"
fi

sudo chown -R ubuntu:ubuntu /data/

if ! cat < /etc/nginx/sites-enabled/default | grep -q "olisabelema.tech"; then
    sudo sed -i '0,/^\(\s*\)server_name\s*.*$/s//\1server_name olisabelema.tech www.olisabelema.tech;/' /etc/nginx/sites-available/default
    sudo sed -i '0,/^\(\s*\)server_name olisabelema.tech www.olisabelema.tech;$/s//&\n\n\1location \/hbnb_static {\n\1\1alias \/data\/web_static\/current\/;\n\1\1autoindex off;\n\1}/' /etc/nginx/sites-available/default
fi

# Restarting Nginx
sudo service nginx restart;

echo "All Done!"
