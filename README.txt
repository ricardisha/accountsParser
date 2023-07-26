sudo apt-get -y install python3 python3-venv python3-dev

sudo apt-get -y install git

git clone <repository>

cd accountsParser

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

export FLASK_APP=main.py

flask db init

(For migrations:
    flask db migrate
    flask db upgrade)

Set settings in .env file

