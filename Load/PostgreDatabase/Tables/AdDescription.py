from Dataclasses import AdvertisementData
from Load.PostgreDatabase.PostgreDatabase import PostgreDatabase

class AdDescription:
    def __init__(self, pg_database: PostgreDatabase) -> None:

        self.pg_database = pg_database

        if self.check_table_existence("ad_description") == False:
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
            CREATE TABLE IF NOT EXISTS ad_description (
            id serial PRIMARY KEY,
            title VARCHAR(255),
            link VARCHAR(255)
            )
        """
        try:
            self.pg_database.execute(query)
            self.pg_database.commit()
        except Exception as e:
            print(f"issue while creating ad_description table: {e}")

    def insert(self, record: AdvertisementData):
        query = """
            INSERT INTO ad_description (title, link)
            VALUES (%(title)s, %(link)s);
            RETURNING id
        """
        #UPSERT should not be needed, since we want records with unique ad_id in fact_table
        self.pg_database.execute(query, {"title": record.title, 
                                         "link": record.link})
        inserted_id = self.pg_database.fetchone()[0]
        self.pg_database.commit()

        return inserted_id


