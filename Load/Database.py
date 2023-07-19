from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import settings


class Database:

    def __init__(self, database, collection_name) -> None:
        self.client = MongoClient(settings.URI, server_api=ServerApi('1'))
        self.db = self.client[database]
        self.collection = self.db[collection_name]
        
        self.collection.create_index("ad_id", unique=True)
    
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