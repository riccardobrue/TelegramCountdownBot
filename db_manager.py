from pymongo import MongoClient
import datetime
import pprint

def initdb():
    client = MongoClient('mongodb://mongodb:mongodbpassword@mongodb/db')
    db = client.db
    try:
        db.create_collection("countdowns")  # create a new collection called "countdowns"
    except:
        pass


    return db.countdowns #get the collection

def add():
    collections=initdb()
    #Add a document in the collection
    countdown = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    collection_id = collections.insert_one(countdown).inserted_id

def get():
    collections=initdb()
    pprint.pprint(collections.find_one({"author": "Mike"}))
    return str(collections.find_one({"author": "Mike"}))