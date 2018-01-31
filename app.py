# THIS IS THE ENTRY POINT FOR OPENSHIFT
from flask import Flask, jsonify
from datetime import datetime
import os
import requests
import random

application = Flask(__name__)

@application.route("/buttonpress")
def press():
    #r = requests.post(urlrow.url, json=details)
    return jsonify({"ButtonPress": "Success"})


if __name__ == "__main__":
    application.run(debug=True)