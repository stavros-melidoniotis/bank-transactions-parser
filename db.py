from os import getenv
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = getenv('MONGODB_URL')
MONGODB_USER = getenv('MONGODB_USER')
MONGODB_PASSWORD = getenv('MONGODB_PASSWORD')
MONGODB_COLLECTION = getenv('MONGODB_COLLECTION')
MONGODB_DATABASE = getenv('MONGODB_DATABASE')

if None in [MONGODB_URL, MONGODB_USER, MONGODB_PASSWORD, MONGODB_COLLECTION, MONGODB_DATABASE]:
    print('Required .env variables not specified! ❌')
    exit(1)

def connect_to_database():
    from pymongo import MongoClient

    CONNECTION_STRING = f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_URL}/?retryWrites=true&w=majority"

    try:
        client = MongoClient(CONNECTION_STRING)
    except:
        print('Failed to connect to MongoDB ❌')
        exit(1)
    else:
        return client[MONGODB_DATABASE]


def get_user_collection(db):
    return db[MONGODB_COLLECTION]

def insert_document(transaction, collection):
    try:
        record_id = collection.insert_one(transaction)
    except:
        print('Insert of document failed ❌')
        exit(1)
    else:
        return record_id