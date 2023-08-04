
from PostgreDatabase import *

class LoadToPostgre:

    def __init__(self, connection_url) -> None:
        self.pg_database = PostgreDatabase(connection_url)


    def insert_record(self):
        # handle fact table (separate class)
        # handle dimensions tables
        pass

