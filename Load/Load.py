from Load.MongoDatabase import MongoDatabase
from Load.PostgreDatabase.LoadToPostgre import LoadToPostgre
import settings

class Load:

    def __init__(self, city) -> None:
        self.city = city
        self.mongo_database = MongoDatabase(settings.DATABASE, city)
        self.load_pg_database = LoadToPostgre()
    

    def load_data(self, data: list):

        #Load to mongoDB
        #self.mongo_database.insert_records(data)

        # TODO postgres load

        self.load_pg_database.pg_database._connect()
        
        self.load_pg_database.initialize_tables()

        for record in data:
            self.load_pg_database.insert_record(record)


        self.load_pg_database.pg_database._disconnect()