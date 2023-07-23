Install virtual enviroment and modules:

python -m venv venv

Linux: source venv/bin/activate
Win: venv\Scripts\activate.bat

pip install -r requirements.txt

export FLASK_APP=main.py

flask db init

(For migrations:
    flask db migrate
    flask db upgrade)

Set settings in .env file

