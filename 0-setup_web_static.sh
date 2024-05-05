#!/usr/bin/env bash
# This script sets up web server for the deployment of web_static
sudo apt update
sudo apt install nginx -y

if [ -d "/data" ]
then
    :
else
    sudo mkdir /data
fi

if [ -d "/data/web_static" ]
then
    :
else
    sudo mkdir /data/web_static
fi

if [ -d "/data/web_static/releases/" ]
then
    :
else
    sudo mkdir /data/web_static/releases/
fi

if [ -d "/data/web_static/shared/" ]
then
    :
else
    sudo mkdir /data/web_static/shared/
fi

if [ -d "/data/web_static/releases/test/" ]
then
    :
else
    sudo mkdir /data/web_static/releases/test/
fi

if [ -e "/data/web_static/releases/test/index.html" ]
then
    :
else
    echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>" | sudo tee -a /data/web_static/releases/test/index.html
fi

if [ -h "/data/web_static/current" ]
then
    :
else
    sudo ln -s /data/web_static/releases/test/ /data/web_static/current
fi

sudo chown -R ubuntu:ubuntu /data

if grep -q "location /hbnb_static" /etc/nginx/sites-available/default
then
    :   
else
    sudo sed -i '/server_name www.omollpeter.tech;/a \
        location /hbnb_static/ {\
                alias /data/web_static/current/;\
        }' /etc/nginx/sites-available/default
fi

sudo service nginx restart
