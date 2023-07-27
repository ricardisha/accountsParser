sudo apt-get -y install python3 python3-venv python3-dev

sudo apt-get -y install git

git clone <repository>

cd accountsParser

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

iptables -A INPUT -p tcp -m tcp --sport 5000 -j ACCEPT
iptables -A OUTPUT -p tcp -m tcp --dport 5000 -j ACCEPT

gunicorn --bind 0.0.0.0:5000 wsgi:app --workers=3



Set settings in .env file

