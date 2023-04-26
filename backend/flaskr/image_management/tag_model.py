import os
import random
from flaskr.db.postgres_db_connect import Connect


class Tag:

    def __init__(self, user, photo:list[str]) -> None:
        self.user = user
        self.photo = photo

    @classmethod

    def add_tags():
        pass   

    def add_bulk_tags():
        pass

    
    def get_tags():
        pass
    
    def delete_tags():
        pass

    def update_tags():
        pass
