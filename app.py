import time, os
from urlparse import urlparse

import flask
import mongoengine
from flask.ext.mongoengine import MongoEngine

from cryptography.fernet import Fernet

# Define our record structure
class Interest(mongoengine.Document):
	email = mongoengine.StringField(required=True)
	referrer = mongoengine.StringField(required=True)
	registered = mongoengine.StringField(required=True)

app = flask.Flask(__name__)

# Set up encryption
app.config['fernet-key'] = os.environ.get("FERNET_KEY")

# Connect to MongoDB
def init_db():
	with app.app_context():
		app.config['MONGO_URI'] = os.environ.get("MONGOHQ_URL", "")
		print "Connecting using URI: %s" % app.config['MONGO_URI']
		app.config['MONGODB_SETTINGS'] = {
			'HOST': app.config['MONGO_URI'],
			'DB': urlparse(app.config['MONGO_URI']).path[1:]
		}
		app.db = MongoEngine(app)
	return app.db

init_db()

@app.route("/interest.js")
def getJS():
	return flask.render_template("interest.js")

@app.route("/interested", methods=['POST'])
def register():
	interest = Interest(email=flask.request.form['email'], referrer=flask.request.form['referrer'], registered=str(time.time()))
	interest.save()
	return "Done"

@app.route("/interested", methods=['GET'])
def list_interested():
	if(not app.config.get('fernet-key', '')):
		return "No encryption key provided. Aborting."
	out = ""
	for x in Interest.objects():
		out += x.email + "\n"
	f = Fernet(app.config['fernet-key'])
	token = f.encrypt(bytes(out))
	return token

if __name__ == "__main__":
	app.run(debug=True)
