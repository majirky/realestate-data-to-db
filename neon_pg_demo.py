import psycopg2
import settings
from Load.PostgreDatabase.PostgreDatabase import *

if __name__ == "__main__":

    # demo that showcases connection to neon serverless postgresql solution

    db = PostgreDatabase()

    query = f"""
            select * from users
            where user_name = %(name)s;
        """
    db.execute(query, {"name": "Robin"})
    result = db.fetchall()
    print(result)

    db._disconnect()





    