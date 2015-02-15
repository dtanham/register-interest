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
app.config['PUBLIC_URI'] = os.environ.get("PUBLIC_URI")

# Connect to MongoDB
def init_db():
	with app.app_context():
		app.config['MONGO_URI'] = os.environ.get("MONGOLAB_URI", "")
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
	return flask.render_template("interest.js", home=app.config.get('PUBLIC_URI')+"/interested")

@app.route("/interested", methods=['POST'])
def register():
	for x in flask.request.form:
		print x
	interest = Interest(email=flask.request.form.get('email',''), referrer=flask.request.form.get('referrer',''), registered=str(time.time()))
	interest.save()
	return flask.redirect(flask.request.form.get('redirectURL','http://www.google.com/'))

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

