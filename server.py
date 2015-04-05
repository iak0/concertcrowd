import os
from nearbyEvents import*
from flask import Flask, render_template, request
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager, Server


app = Flask(__name__)

# app.config["MONGODB_SETTINGS"] = {'DB': "concertcrowd"}
app.config["MONGODB_SETTINGS"] = {'DB': "concertcrowd", 'host':'mongodb://ds061371.mongolab.com/heroku_app35547130', 'port': 61371}

app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True)
)

@app.route('/', methods = ["GET"])
def login():
    return render_template('index.html')

@app.route('/home', methods = ["GET"])
def home():
	#location zipCode
	zipCode = '95128'
	#e1,e2 = nearbyEvents(zipCode)
	e1,e2 = [],[]
	return render_template('home.html', events1=e1, events2=e2)

if __name__ == '__main__':
    app.debug = True
    manager.run()