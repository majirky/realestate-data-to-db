from Load.Database import Database
import settings

class Load:

    def __init__(self, city) -> None:
        self.database = Database(settings.DATABASE, city)