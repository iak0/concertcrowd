import os
from flask import Flask, render_template, request
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager, Server


app = Flask(__name__)
app.debug = True
if app.debug:
    app.config["MONGODB_SETTINGS"] = {'DB': "concertcrowd"}
else:
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
def home():
    return render_template('index.html', time = "", author = "", genre = "", song_id = "0", play = "false")

if __name__ == '__main__':
    app.debug = True
    manager.run()