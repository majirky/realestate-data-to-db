from Load.MongoDatabase import MongoDatabase
from Load.PostgreDatabase.LoadToPostgre import LoadToPostgre
import settings

class Load:

    def __init__(self, city) -> None:
        self.city = city
        self.mongo_database = MongoDatabase(settings.DATABASE, city)
        self.load_pg_database = LoadToPostgre(settings.PG_DATABASE_URL)
    

    def load_data(self, data):

        #Load to mongoDB
        #self.mongo_database.insert_records(data)

        # TODO postgres load
        # TODO call LoadToPostgre method here, but make for loop also here in case of multithreading implementation
        for record in data:
            print(record)