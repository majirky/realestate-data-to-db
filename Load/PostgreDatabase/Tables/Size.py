from Dataclasses import AdvertisementData
from Load.PostgreDatabase.PostgreDatabase import PostgreDatabase

class Size:
    def __init__(self, pg_database: PostgreDatabase) -> None:

        self.pg_database = pg_database

        if self.check_table_existence("size") == False:
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
            CREATE TABLE IF NOT EXISTS size (
            id serial PRIMARY KEY,
            living_area FLOAT,
            land_area FLOAT,
            price_per_meter FLOAT
            )
        """
        try:
            self.pg_database.execute(query)
            self.pg_database.commit()
        except Exception as e:
            print(f"issue while creating ad_description table: {e}")


    def insert(self, record: AdvertisementData) -> int:
        query = """
            INSERT INTO size (living_area, land_area, price_per_meter)
            VALUES (%(living_area)s, %(land_area)s, %(price_per_meter)s)
            RETURNING id;
        """
        #UPSERT should not be needed, since we want records with unique ad_id in fact_table
        self.pg_database.execute(query, {"living_area": record.living_area,
                                         "land_area": record.land_area,
                                         "price_per_meter": record.price_per_meter})
        inserted_id = int(self.pg_database.fetchone()[0])
        #commit is in fact_table insert

        return inserted_id