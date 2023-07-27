sudo apt-get -y install python3 python3-venv python3-dev

sudo apt-get -y install git

git clone <repository>

cd accountsParser

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

sudo ufw allow 5000

uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

You’re now done with your virtual environment, so you can deactivate it:

deactivate

nano ~/accountsParser/accountsParser.ini

Paste in file:
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = accountsParser.sock
chmod-socket = 660
vacuum = true

die-on-term = true

sudo nano /etc/systemd/system/accountsParser.service

Paste in file:

[Unit]
Description=uWSGI instance
After=network.target

[Service]
User=...
Group=www-data
WorkingDirectory=/home/<User>/myproject
Environment="PATH=/home/<User>/accountsParser/venv/bin"
ExecStart=/home/<User>/accountsParser/venv/bin/uwsgi --ini accountsParser.ini

[Install]
WantedBy=multi-user.target

Change options in file(User and <User>)

sudo chgrp www-data /home/<User>

Configuring Nginx:

sudo nano /etc/nginx/sites-available/accountsParser

Paste in this file:
server {
    listen 80;
    server_name your_domain www.your_domain;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/<User>/accountsParser/accountsParser.sock;
    }
}

Change some options here.

sudo ln -s /etc/nginx/sites-available/accountsParset /etc/nginx/sites-enabled

sudo unlink /etc/nginx/sites-enabled/default

sudo systemctl restart nginx

No longer need access through port 5000, so you can remove that rule. Then, you can allow access to the Nginx server:

sudo ufw delete allow 5000
sudo ufw allow 'Nginx Full'
