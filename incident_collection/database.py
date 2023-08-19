from pymongo import mongo_client, ASCENDING, MongoClient
from pymongo.collection import Collection
from config import DB_HOST, DB_PORT, DB_NAME


client: MongoClient = MongoClient(f"{DB_NAME}://{DB_HOST}:{DB_PORT}/")

db = client.collection