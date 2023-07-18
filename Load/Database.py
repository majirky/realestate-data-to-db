from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import settings


class Database:

    def __init__(self) -> None:
        self.client = MongoClient(settings.URI, server_api=ServerApi('1'))
        self.db = self.client["real_estate_db"]
        self.collection = self.db["Kosice"]
    
    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    
    def insert_many(self, data: list):
        try:
            self.collection.insert_many(data)
        except Exception as e:
            print(f"problem while inserting data into mongoDB {e}")