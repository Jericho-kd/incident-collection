from pymongo import MongoClient
from pymongo.collection import Collection

from config import DB_HOST, DB_PORT, DB_NAME


client: MongoClient = MongoClient(f"{DB_NAME}://{DB_HOST}:{DB_PORT}/")

db = client.collection
collection: Collection[dict[str, str | list[dict[str, str]]]] = db.incidents

collection.create_index([("header.key", 1), ("header.value", 1)])
collection.create_index([("body.key", 1), ("body.value", 1)])
collection.create_index(["hash"])