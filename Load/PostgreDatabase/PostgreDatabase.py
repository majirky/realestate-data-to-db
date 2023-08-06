import psycopg2
import settings

class PostgreDatabase:

    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
        return self._instance
    
    def __init__(self) -> None:
        try:
            self.connection = psycopg2.connect(settings.PG_DATABASE_URL)
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Problem with connecting to Neon-PostgreSQL: {e}")


    def _disconnect(self):
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(f"Problem with closing connection: {e}")

    
    def commit(self):
        try:
            self.connection.commit()
        except Exception as e:
            print(f"Problem with commiting changes to DB: {e}")


    def execute(self, query: str, *args):
        try:
            self.cursor.execute(query, *args)
        except Exception as e:
            print(f"Problem with executing query: {e}")


    def fetchone(self):
        result = None
        try:
            result = self.cursor.fetchone()
        except Exception as e:
            print(f"Problem with fetching one: {e}")
        return result
    

    def fetchall(self):
        result = None
        try:
            result = self.cursor.fetchall()
        except Exception as e:
            print(f"Problem with fetching all: {e}")
        return result