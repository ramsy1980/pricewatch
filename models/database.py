from pymongo import MongoClient

class Database:
    def __init__(self, uri: str):
        self.uri = uri
        self.client = MongoClient(self.uri)
        self.db = self.client.pricewatch
