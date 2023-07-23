import os
import re
import json
import requests
import schedule
from flask import Flask, request, redirect, url_for, session, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2
from dotenv import load_dotenv
from DB import dbClass
from models import Accounts, MyModelView


load_dotenv()

host = os.getenv("HOST_DB")
username = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD_DB")
dbName = os.getenv("DB_NAME")
adminLogin = os.getenv("ADMIN_LOGIN")
adminPassword = os.getenv("ADMIN_PASSWORD")


app = Flask(__name__)


app.config['FLASK_ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:5432/{dbName}"
app.config['SECRET_KEY'] = 'asd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

dataBase = dbClass(host=host, user=username, password=password, database=dbName)



@app.route("/", methods = ['POST'])
def mainPage():
	
	data = ''
	error_code = 0
	error_message = ''

	requestRes = request.get_json()

	query = requestRes['query']
	language = requestRes['language']
	countPages = requestRes['countPages']
	timep = requestRes['timep']
	result_accuracy = requestRes['result_accuracy']

	req = query.replace(" ", "+").strip()

	baseCountPages = 1

	config_api_info = dataBase.get_couple_info()

	hrefsArr = []

	descsArr = []

	for i in range(int(countPages)):

		curCoupleApi = 0

		if ((baseCountPages // 9) > 1) and (baseCountPages % 9 == 1):
			
			dataBase.set_unavailable_status_of_couple(curCoupleApi + 1)

			curCoupleApi += 1	

		numRes = 10

		start = (baseCountPages - 1) * 9 + 1

		if config_api_info[curCoupleApi] not in config_api_info:

			error_message = "The number of pairs for the day is over"

			error_code = 1
			
			break

		url = f"https://www.googleapis.com/customsearch/v1?key={config_api_info[curCoupleApi][0]}&cx={config_api_info[curCoupleApi][1]}&q={req}+site%3Ainstagram.com&start={start}&num={numRes}&siteSearch=https://www.instagram.com/reel/&siteSearch=https://www.www.instagram.com/reels/&siteSearch=https://www.instagram.com/p/&siteSearchFilter=e"
		url = url + f"&lr=lang_{language}" if language else url
		url = url + f"&dateRestrict={timep}" if timep else url
		url = url + f"&exactTerms={req}" if result_accuracy != "all" else url

		resOfSearch = requests.get(url).json()

		if 'error' in resOfSearch:

			error_message = resOfSearch['error']['message']

			error_code = 1

			break

		else:

			search_items = resOfSearch.get("items")
		
			for i, search_item in enumerate(search_items, start=1):

				snippet = search_item.get("snippet")

				link = search_item.get("link")

				hrefsArr.append(link)

				descsArr.append(snippet)

		
			baseCountPages += 1
		

	allInfoArr = []

	updDescsArr = []

	for res in descsArr:
		subs = re.search(r"\d+([MK])? (f|F)ollowers", res)

		posts = re.search(r"\d+([MK])? (p|P)osts", res)

		if subs != None and posts != None:
			updDescsArr.append({
				'subscribers': subs.group(0),
				'posts': posts.group(0)
			})
		else:
			updDescsArr.append("Nope")

	for i in range(0, len(hrefsArr) - 1):
		allInfoArr.append({
			'href': hrefsArr[i],
			'info': updDescsArr[i]
		})

	data = json.dumps(allInfoArr)
		
	return [data, error_code, error_message]


@app.route('/login', methods=['GET', 'POST'])
def login():

	message = ''

	if request.method == "POST" and 'username' in request.form and 'password' in request.form:
		username = request.form['username']

		password = request.form['password']

		if username == adminLogin and password == adminPassword:
			session['loggedin'] = True

			message = "You're Logged In!"

		else:
			message = 'Please enter correct username / password !'

	return render_template('login.html', message=message)

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('login'))

def scheduleRun():
	schedule.every().day.at("00:00").do(dataBase.set_available_status_of_couple)

admin = Admin(app)
admin.add_view(MyModelView(Accounts, db.session))
	


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(host='0.0.0.0', debug=True)