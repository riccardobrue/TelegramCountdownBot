# THIS IS THE ENTRY POINT FOR OPENSHIFT
from flask import Flask, jsonify
from datetime import datetime
import os
import requests
import random

user = os.environ["MYSQL_USER"]
passwd = os.environ["MYSQL_PASSWORD"]
dbhost = os.environ["MYSQL_SERVICE_HOST"]
dbname = os.environ["MYSQL_DATABASE"]

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql://%s:%s@%s/%s' % (user, passwd, dbhost, dbname)

application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@application.route("/buttonpress")
def press():
    #r = requests.post(urlrow.url, json=details)
    return jsonify({"ButtonPress": "Success"})


if __name__ == "__main__":
    application.run(debug=True)