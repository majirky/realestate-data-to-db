from Dataclasses import AdvertisementData
from Load.PostgreDatabase.PostgreDatabase import PostgreDatabase

class FactTable:
    def __init__(self, pg_database: PostgreDatabase) -> None:

        self.pg_database = pg_database

        if self.check_table_existence("fact_table") == False:
            self.create_table()


    def check_table_existence(self, table_name):
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
            CREATE TABLE IF NOT EXISTS fact_table (
            ad_id INT UNIQUE,
            id_description INT,
            FOREIGN KEY (id_description) REFERENCES ad_description (id) ON DELETE CASCADE
            )
        """
        try:
            self.pg_database.execute(query)
            self.pg_database.commit()
        except Exception as e:
            print(f"issue while creating ad_description table: {e}")

    
    def insert(self, record: AdvertisementData, foreign_keys: dict) -> int:
        data = {
            "ad_id": record.ad_id,
            "id_description": foreign_keys["ad_description_id"]
        }
        #TODO add date column.
        query = """
            INSERT INTO fact_table (ad_id, id_description)
            VALUES (%(ad_id)s, %(ad_description_id)s);
            RETURNING ad_id
        """
        self.pg_database.execute(query, data)
        inserted_ad_id = self.pg_database.fetchone()[0]
        self.pg_database.commit()

        return int(inserted_ad_id)