from Dataclasses import AdvertisementData
from Load.PostgreDatabase.PostgreDatabase import PostgreDatabase

class CityAreas:
    def __init__(self, pg_database: PostgreDatabase) -> None:

        self.pg_database = pg_database

        if self.check_table_existence("city_areas") == False:
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
            CREATE TABLE IF NOT EXISTS city_areas (
            id serial PRIMARY KEY,
            name VARCHAR(255)
            )
        """
        try:
            self.pg_database.execute(query)
            self.pg_database.commit()
        except Exception as e:
            print(f"issue while creating Cities table: {e}")
    

    def get_or_insert(self, record: AdvertisementData):
        query = """
            Select name 
            FROM city_areas
            WHERE name == %(name)s;
        """
        self.pg_database.execute(query, {"name": record.city_area})
        inserted_id = self.pg_database.fetchone()
        if inserted_id is None:
            return self.insert(record)
        else:
            return int(inserted_id[0])


    def insert(self, record: AdvertisementData) -> int:
        query = """
            INSERT INTO city_areas (name)
            VALUES (%(name)s)
            RETURNING id;
        """
        #UPSERT should not be needed, since we want records with unique ad_id in fact_table
        self.pg_database.execute(query, {"name": record.city_area})
        inserted_id = int(self.pg_database.fetchone()[0])
        #commit is in fact_table insert

        return inserted_id