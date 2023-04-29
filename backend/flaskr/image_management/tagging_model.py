from flaskr.db.postgres_db_connect import Connect
import pandas as pd
from celery import Celery
import psycopg2


def db_temp_connection():
        try: 
            conn =  Connect.get_connection()
            cursor =conn.cursor()
            print("DB connection sucessful")
          
    
        
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            print("failed connection")
        return cursor


class Taging:

    def __init__(self, tag_id, img_id) -> None:
        self.tag_id = tag_id
        self.img_id = img_id

    @classmethod

    def add_tags(cs, tag_id, img_id):
        add_tag_query = f'INSERT INTO tagging (tag_id, img_id) VALUES("{tag_id}","{img_id}");'
        try:
            cursor = db_temp_connection()
            cursor.execute()
            cursor.close()
            print(f"Tag: {tag_id} added to photo: {img_id}")
        except Exception as e:
            print(e)
            print(f'Addition of tag: {tag_id} to photo:{img_id} failed')
        

    def add_bulk_tags_to_dir(cs, dir_id, tag_id):
        try:
            bulk_query = f'SELECT photo_id FROM (imgdirectories INNER JOIN photo ON id = photo_directory ) WHERE id = "{dir_id}";'
            cursor= db_temp_connection()
            cursor.execute(bulk_query)
            photos_in_dir = pd.DataFrame(cursor.fetchall(), columns='photo_id')
            photos_in_dir['tag_id'] = tag_id
            photos_in_dir.to_sql('tagging',con=cursor)
        
        except Exception as e:
             print(e)
             print('Failed bulk tagging')


    
    def get_taged_img(cs, tag_id, img_id):
       
        tagged_query = f'SELECT * FROM tagging WHERE tag_id = "{tag_id}", img_id = "{img_id}";'
        
        try: 
            cursor = db_temp_connection()
            cursor.execute(tagged_query)
            query_df = pd.DataFrame(cursor.fetchall())
            cursor.close()
    
        
        except Exception as e:
            print(e)
            print(f"no image:{img_id} with tag:{tag_id} ")
    
        return query_df
        
   
    
    def delete_tags(cs, tag_id, img_id):
        del_query = f'DELETE FROM taging WHERE tag_id= "{tag_id}", img_id = "{img_id}";'
        cursor =db_temp_connection()
        try:
                 cursor.execute(del_query)
                 cursor.close()
                 print('Tag Deleted')
        
        except Exception as e:
                 print(e)
                 print("no tag exist")
       
        return " "
    
    



