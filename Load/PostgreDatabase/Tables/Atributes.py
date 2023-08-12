from Dataclasses import AdvertisementData
from Load.PostgreDatabase.PostgreDatabase import PostgreDatabase

class Atributes:
    def __init__(self, pg_database: PostgreDatabase) -> None:

        self.pg_database = pg_database

        if self.check_table_existence("atributes") == False:
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
            CREATE TABLE IF NOT EXISTS atributes (
            id serial PRIMARY KEY,
            housing VARCHAR(128),
            housing_category VARCHAR(128),
            housing_type VARCHAR(128),
            housing_state VARCHAR(128)
            )
        """
        try:
            self.pg_database.execute(query)
            self.pg_database.commit()
        except Exception as e:
            print(f"issue while creating atributes table: {e}")

    
    def insert(self, record: AdvertisementData):
        query = """
            INSERT INTO atributes (housing, housing_category, housing_type, housing_state)
            VALUES (%(housing)s, %(housing_category)s, %(housing_type)s, %(housing_state)s)
            RETURNING id;
        """
        #UPSERT should not be needed, since we want records with unique ad_id in fact_table
        self.pg_database.execute(query, {"housing": record.housing, 
                                         "housing_category": record.housing_category,
                                         "housing_type": record.housing_type,
                                         "housing_state": record.housing_state
                                         })
        inserted_id = int(self.pg_database.fetchone()[0])
        #commit is in fact_table insert

        return inserted_id