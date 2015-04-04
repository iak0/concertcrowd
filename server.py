import os
from flask import Flask, render_template, request
from urllib2 import urlopen
from xml.dom import minidom
from random import choice

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def home():
    return render_template('index.html', time = "", author = "", genre = "", song_id = "0", play = "false")


if __name__ == '__main__':
    app.debug = True
    app.run()