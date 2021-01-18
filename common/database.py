import os
from pymongo import MongoClient, CursorType
from typing import Dict


class Database:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = MongoClient(self.uri)
        self.db = self.client.get_database()
    
    def insert(self, collection: str, data: Dict):
        self.db[collection].insert(data)
    
    def find(self, collection: str, query: Dict) -> CursorType :
        return self.db[collection].find(query)

    def find_one(self, collection: str, query: Dict) -> Dict:
        return self.db[collection].find_one(query)

    def update(self, collection: str, query: Dict,  data: Dict) -> None:
        return self.db[collection].update(query, data, upsert=True)

    def remove(self, collection: str, query: Dict) -> Dict:
        return self.db[collection].remove(query)


database = Database(os.environ.get("MONGODB_URI"))
