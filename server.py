import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.mongoengine import MongoEngine
from flask.ext.script import Manager, Server

import requests
from rauth import OAuth1Session

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
    return render_template('home.html', hits="")

@app.route('/home', methods = ["POST"])
def context():
    email, password = request.form["email"], request.form["password"]  
    
    CONSUMER_KEY = '1lpx2bez'
    CONSUMER_SECRET = 'rkCatV0VIxUA6gDm'
    session = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET)

    query = session.request('GET', "https://api.context.io/2.0/accounts/", header_auth=True, params={'email': email}, headers={})
    if query.json() == []:
        email, password = request.form["email"], request.form["password"]  
        print("not found")
        if "aol" in email:
            server = "imap.aol.com"
            port = 993
        if "yahoo" in email:
            server = "imap.yahoo.com"
            port = 993
        acc = session.request('POST', "https://api.context.io/2.0/accounts", header_auth=True, data={'email': email}, headers={})
        mailbox_params = {'label': 0, 'email': email, 'password':password, 'type':"IMAP",
                         "use_ssl":"1", "username":email, "server":server, "port":port}
        id = acc.json()["id"]
        box = session.request('POST', "https://api.context.io/2.0/accounts/"+id+"/sources", header_auth=True, data=mailbox_params, headers={})
        print(acc.json())
        print(box.json())
    else:
        print("found")
        print(query.json())
        id = query.json()[0]["id"]

    search_params = {"subject":"/concert|Ticketmaster|Stubhub/", "include_body":1}
    search = session.request('GET', "https://api.context.io/2.0/accounts/"+id+"/messages", header_auth=True, params=search_params, headers={})
    hits = [hit["subject"]+hit["body"][0]["content"][:500] for hit in search.json()]
    print(hits)
    return render_template('home.html', hits=hits)

if __name__ == '__main__':
    app.debug = True
    manager.run()