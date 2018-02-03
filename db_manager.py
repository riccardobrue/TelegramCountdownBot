from pymongo import MongoClient
import datetime
import pprint



def initdb():
    #client = MongoClient('mongodb://mongodb:mongodbpassword@mongodb/db') #from openshift
    client = MongoClient('mongodb://localhost:27017/db') #local

    db = client.db
    try:
        db.create_collection("countdowns")  # create a new collection called "countdowns"
    except:
        pass

    return db.countdowns #get the collection

def add(chatId, chatName, message, date, counter):
    collections=initdb()
    record = collections.find_one({'chartid': chatId, 'chatName': chatName, 'counter': counter})

    if (record == None):
        targetDate = datetime.datetime.strptime(date, '%d/%m/%Y')
        today = datetime.datetime.utcnow()

        if(today<targetDate):
            # Add a document in the collection
            countdown = {"chartid": chatId,
                         "chatName": chatName,
                         "message":message,
                         "date": targetDate,
                         "counter": counter}

            insertedId=collections.insert_one(countdown).inserted_id
            return "Date saved for the countdown!"
        else:
            return "Cannot countdown to the past!"

    else:
        return add(chatId, chatName, message, date, counter+1)



def edit(chatId, chatName, newmessage, newdate, counter):
    collections = initdb()
    record = collections.find_one({'chartid': chatId, 'chatName': chatName, 'counter': counter})

    if (record == None):
        return "Cannot find the countdown!"
    else:
        return "TO DO!"



def get(chatId,chatName,counter):
    collections=initdb()
    record=collections.find_one({'chartid': chatId, 'chatName': chatName, 'counter': counter})
    if(record==None):
        return "None object found"
    else:
        pprint.pprint(record)

    return str(record)