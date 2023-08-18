from pymongo import mongo_client, ASCENDING, MongoClient


client: MongoClient = MongoClient("mongodb://localhost:27017/")

db = client["incidents"]