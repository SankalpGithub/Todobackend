import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MongodbConString = os.getenv('MongodbConString')

def con(): 
    try:
        MyClient = pymongo.MongoClient(MongodbConString)
        if "TodoApp" in MyClient.list_database_names():
            return MyClient['TodoApp']
    except Exception as e:
        # Handle multiple exceptions
        return e