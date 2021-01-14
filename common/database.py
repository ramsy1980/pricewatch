import os
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import Dict

class Database:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = MongoClient(self.uri)
        self.db = self.client.get_database()
    
    def insert(self, collection: str, data: Dict):
        self.db[collection].insert(data)

database = Database(os.environ.get("MONGODB_URI"))
