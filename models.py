from main import db
from flask_admin.contrib.sqla import ModelView
from flask import session

class Accounts(db.Model):
	__tablename__ = "accounts"

	id = db.Column(db.Integer, primary_key=True)
	api_key = db.Column(db.Text)
	search_engine_id = db.Column(db.Text)
	status_of_couple = db.Column(db.Text, default="available")

class MyModelView(ModelView):
	def is_accessible(self):
		if 'loggedin' in session:
			return True
		else:
			return False