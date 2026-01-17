from pymongo import MongoClient
import os

mongo_url = os.getenv("MONGODB_URL")

client = MongoClient(mongo_url)
db = client["Ais-travel-guide"]
Users = db["users"]

Users.create_index({"username": 1})
