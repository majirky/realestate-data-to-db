from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import DuplicateKeyError
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

    
    def insert_records(self, data: list):
        """inserts list of dictionaries into mongoDB

        Args:
            data (list): list of dictionaries of data, that should be insertet into colection.
        """
        for record in data:
            try:
                self.collection.insert_one(record)
            except DuplicateKeyError:
                print(f"Skipped (duplicate): {record['ad_id']}")
            except Exception as e:
                print(f"problem while inserting data into mongoDB {e}")