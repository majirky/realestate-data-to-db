from Dataclasses import AdvertisementData
from Load.PostgreDatabase.PostgreDatabase import PostgreDatabase
from psycopg2.errors import UniqueViolation

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
            id_size INT,
            id_locations INT,
            id_atributes INT,
            price FLOAT,
            date BIGINT,
            FOREIGN KEY (id_description) REFERENCES ad_description (id) ON DELETE CASCADE,
            FOREIGN KEY (id_size) REFERENCES size (id) ON DELETE CASCADE,
            FOREIGN KEY (id_atributes) REFERENCES atributes (id) ON DELETE CASCADE
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
            "id_description": foreign_keys["id_description"],
            "id_size": foreign_keys["id_size"],
            "id_locations": foreign_keys["id_locations"],
            "id_atributes": foreign_keys["id_atributes"],
            "price": record.price,
            "date": record.date
        }

        query = """
            INSERT INTO fact_table (ad_id, id_description, id_size, id_locations, id_atributes, price, date)
            VALUES (%(ad_id)s, %(id_description)s, %(id_size)s, %(id_locations)s, %(id_atributes)s, %(price)s, %(date)s)
            RETURNING ad_id;
        """
        inserted_ad_id = None
        try:
            self.pg_database.execute(query, data)
            inserted_ad_id = self.pg_database.fetchone()
            self.pg_database.commit()
        except UniqueViolation as e:
            print(f"record for ad with id {record.ad_id} is already in DB.")
            self.pg_database.rollback()
        except Exception as e:
            print(f"problem with inserting into fact table: {e}")
            self.pg_database.rollback()
        else:
            inserted_ad_id = int(inserted_ad_id[0])
            print(f"inserted record with ad_ID: {inserted_ad_id} to neon Postgre")
            #logger

        return inserted_ad_id