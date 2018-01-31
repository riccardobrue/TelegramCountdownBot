# THIS IS THE ENTRY POINT FOR OPENSHIFT
from flask import Flask, jsonify
from datetime import datetime
import os
import requests
import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route("/b")
def press():
    #r = requests.post(urlrow.url, json=details)
    return jsonify({"ButtonPress": "Success"})


if __name__ == "__main__":
    app.run()