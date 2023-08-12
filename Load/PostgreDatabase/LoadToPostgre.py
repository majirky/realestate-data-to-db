from Load.PostgreDatabase.PostgreDatabase import *
from Load.PostgreDatabase.Tables.AdDescription import *
from Load.PostgreDatabase.Tables.FactTable import *
from Load.PostgreDatabase.Tables.Size import *
from Load.PostgreDatabase.Tables.Location import *
from Load.PostgreDatabase.Tables.Atributes import *
from Dataclasses import AdvertisementData

class LoadToPostgre:

    def __init__(self) -> None:
        self.pg_database = PostgreDatabase()
        

    def initialize_tables(self):
        self.ad_description = AdDescription(self.pg_database)
        self.size = Size(self.pg_database)
        self.locations = Locations(self.pg_database)
        self.fact_table = FactTable(self.pg_database)
        self.atributes = Atributes(self.pg_database)
    

    def insert_record(self, record: AdvertisementData):
        # TODO if I delete record from one dimension, record in fact table will be deleted, 
        # but record for that ad will stay in onther dimensions, how to delete that?
        record_foregin_keys = {}

        record_foregin_keys["id_description"] = self.ad_description.insert(record)
        record_foregin_keys["id_size"] = self.size.insert(record)
        record_foregin_keys["id_locations"] = self.locations.insert(record)
        record_foregin_keys["id_atributes"] = self.atributes.insert(record)


        inserted_ad_id = self.fact_table.insert(record, record_foregin_keys)



