from pymongo import MongoClient
import datetime
import pprint

def start():
    client = MongoClient('mongodb://mongodb:mongodbpassword@mongodb/db')
    db = client.db

    db.create_collection("countdowns") #create a new collection called "countdowns"
    return db.countdowns #get the collection

def add():
    collections=start()
    #Add a document in the collection
    countdown = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}

    collection_id = collections.insert_one(countdown).inserted_id

def get():
    collections=start()
    pprint.pprint(collections.find_one({"author": "Mike"}))
    return str(collections.find_one({"author": "Mike"}))