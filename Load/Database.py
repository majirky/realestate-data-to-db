from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import settings


class Database:

    def __init__(self) -> None:
        self.client = MongoClient(settings.URI, server_api=ServerApi('1'))
    
    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)