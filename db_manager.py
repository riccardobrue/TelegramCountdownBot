from pymongo import MongoClient
import datetime

def initdb():
    client = MongoClient('mongodb://mongodb:mongodbpassword@mongodb/db')    #from OpenShift
    #client = MongoClient('mongodb://localhost:27017/db')                   #local

    db = client.db
    try:
        db.create_collection("countdowns")  # create a new collection called "countdowns"
    except:
        pass
    return db.countdowns #get the collection


def add(chatId, chatName, message, date, counter):
    collection=initdb()
    record = collection.find_one({'chartid': chatId, 'chatName': chatName, 'counter': counter})
    if (record == None):
        targetDate = datetime.datetime.strptime(date, '%d/%m/%Y')
        today = datetime.datetime.utcnow()

        if(today<targetDate):
            # Add a document in the collection
            if(message==None):
                countdown = {"chartId": chatId,
                             "chatName": chatName,
                             "date": targetDate,
                             "counter": counter}
            else:
                countdown = {"chartId": chatId,
                             "chatName": chatName,
                             "message":message,
                             "date": targetDate,
                             "counter": counter}

            insertedId=collection.insert_one(countdown).inserted_id
            #SET THE NEXT COUNTDOWN
            return "Date saved for the countdown!"
        else:
            return "Cannot countdown to the past!"

    else:
        return add(chatId, chatName, message, date, counter+1)



def edit(chatId, chatName, newmessage, newdate, counter):
    collection = initdb()
    record = collection.find_one({'chartid': chatId, 'chatName': chatName, 'counter': counter})
    if (record == None):
        return "Cannot find the countdown!"
    else:
        targetDate = datetime.datetime.strptime(newdate, '%d/%m/%Y')
        today = datetime.datetime.utcnow()

        if(today<targetDate):
            countdown = {"chartid": chatId,
                         "chatName": chatName,
                         "message": newmessage,
                         "date": targetDate,
                         "counter": counter}

            collection.update_one({'_id': record["_id"] }, {"$set": countdown})
            # SET THE NEXT COUNTDOWN
            return "Record updated!"
        else:
            return "Cannot countdown to the past!"


def getSingle(chatId,chatName,counter):
    collection=initdb()
    record=collection.find_one({'chartid': chatId, 'chatName': chatName, 'counter': counter})
    if(record==None):
        return "None object found"
    else:
        return str(record)

def getAll(chatId,chatName):
    collection=initdb()
    record=collection.find({'chartid': chatId, 'chatName': chatName})
    if(record==None):
        return "None object found"
    else:
        return record