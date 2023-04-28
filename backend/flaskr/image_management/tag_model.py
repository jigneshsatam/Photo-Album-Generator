import os
import random
from flaskr.db.postgres_db_connect import Connect
import pandas as pd
from celery import Celery
import psycopg2


def db_connection():
        try: 
            conn =  Connect.get_connection()
            cursor =conn.cursor()
            print("DB connection sucessful")
          
    
        
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            print("failed connection")
        return cursor


class Tag:

    def __init__(self, user, photo:list[str]) -> None:
        self.user = user
        self.photo = photo

    @classmethod

    def add_tags(cs, user_id, photo_location, tag):
        
        
        pass   

    def add_bulk_tags_to_dir(cs, tag, directory):
        bulk_query = ""
        pass

    
    def get_tags(cs, user):
       
        tag_query = f'SELECT userid, tag, foto_dir FROM tags WHERE userid = {user}'
        
        try: 
            cursor = db_connection()
            cursor.execute(tag_query)
            query_df = pd.DataFrame(cursor.fetchall())
            conn.close()
    
        
        except (Exception) as e:
            print(e)
            print("failed query")
    
        return query_df
        
   
    
    def delete_tags(cs, user, tags, directory):
        del_query = f"DELETE {tags} FROM tags WHERE uersid = {user}, directory = {directory}"
        cursor =db_connection()
        try:
                 cursor.execute(del_query)
                 cursor.close()
                 print('Tag Deleted')
        
        except Exception as e:
                 print(e)
                 print("no tag exist")
       
        return " "
    
    
    def update_tags(cs):
        pass



