import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

# Load from .env file
load_dotenv(find_dotenv())

class Connect:
    cnxn = None

    @classmethod
    def get_connection(self):
        if self.cnxn is not None:
            return self.cnxn
        self.cnxn = psycopg2.connect(os.getenv('Postgres_DB_Connection_String'))
        return self.cnxn