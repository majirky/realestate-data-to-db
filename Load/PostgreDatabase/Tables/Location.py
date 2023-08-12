from Dataclasses import AdvertisementData
from Load.PostgreDatabase.PostgreDatabase import PostgreDatabase
from Load.PostgreDatabase.Tables.Cities import *
from Load.PostgreDatabase.Tables.CityAreas import *

class Locations:
    def __init__(self, pg_database: PostgreDatabase) -> None:

        self.pg_database = pg_database

        self.cities = Cities(pg_database)
        self.city_areas = CityAreas(pg_database)

        if self.check_table_existence("location") == False:
            self.create_table()


    def check_table_existence(self, table_name: str):
        query = """
            SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'table_name'
            ) AS table_existence;
        """
        self.pg_database.execute(query, {"table_name": table_name})
        exists = self.pg_database.fetchone()
        return exists[0]
    

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS locations (
            id serial PRIMARY KEY,
            lat NUMERIC(10, 7),
            long NUMERIC(10, 7),
            id_city INT,
            id_city_area INT,
            FOREIGN KEY (id_city) REFERENCES cities (id) ON DELETE CASCADE,
            FOREIGN KEY (id_city_area) REFERENCES city_areas (id) ON DELETE CASCADE
            )
        """
        try:
            self.pg_database.execute(query)
            self.pg_database.commit()
        except Exception as e:
            print(f"issue while creating Locations table: {e}")
    

    def insert(self, record: AdvertisementData) -> int:
        query = """
            INSERT INTO locations (lat, long, id_city, id_city_area)
            VALUES (%(lat)s, %(long)s, %(id_city)s, %(id_city_area)s)
            RETURNING id;
        """
        #UPSERT should not be needed, since we want records with unique ad_id in fact_table
        self.pg_database.execute(query, {"lat": record.lat, 
                                         "long": record.long,
                                         "id_city": self.cities.get_or_insert(record),
                                         "id_city_area": self.city_areas.get_or_insert(record)
                                         }
                                )
        inserted_id = int(self.pg_database.fetchone()[0])
        #commit is in fact_table insert

        return inserted_id