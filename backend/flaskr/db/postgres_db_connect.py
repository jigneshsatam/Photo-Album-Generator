import os
import psycopg2

class Connect:
    cnxn = None

    @classmethod
    def get_connection(self):
        if self.cnxn is not None:
            return self.cnxn
        self.cnxn = psycopg2.connect('postgresql://photogendocker:photogendocker@database:5432/photogen')
        return self.cnxn