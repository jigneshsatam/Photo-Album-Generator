import os
import random
from flaskr.db.postgres_db_connect import Connect
import logging

# from .image_model import Image

class Image:
  path: str = None
  tags: list[str] = []

  def __init__(self, path: str, tags: list[str]) -> None:
    self.path = path
    self.tags = tags

  @classmethod
  def get_images(cls, directory: str) -> list:
    images: list[Image] = []

    dummy_tags: list[list[str]] = [
        ["Test-1", "Test-3", "Test-5", "Test-7"],
        ["Test-2", "Test-4", "Test-6", "Test-8"],
        ["Test-9", "Test-10"],
    ]

    # get images
    for img in os.scandir(directory):
      if img.name.endswith(".png") or img.name.endswith(".jpg") or img.name.endswith(".jpeg"):
        images.append(Image(img.path, random.choice(dummy_tags)))

    return images
  
  def add_new_directory(user_id, dir_path):
    #logging.warning('Start add new directory function')
    result = False
    dir_id = -1

    try:
      conn = Connect().get_connection()

      # Create cursor to perform database operations
      cursor = conn.cursor()

      # Insert new directory path
      query = "insert into imgdirectories(userid, dirpath) values(" + str(user_id) + ", '" + dir_path + "') returning id"     
      #logging.warning(query) 
      cursor.execute(query)
      
      # Get id for new directory path
      dir_id = int(cursor.fetchone()[0])
      
      conn.commit()

      #conn.close()
      cursor.close()
      
      result = True
    except Exception as e:
      logging.error(e)
      result = False
      
    return dir_id, result
  
  def get_albums():
    result = False
    albums = []

    try:
      conn = Connect().get_connection()

      # Create cursor to perform database operations
      cursor = conn.cursor()

      query = "SELECT * FROM imgdirectories"     
      
      cursor.execute(query)
      
      for row in cursor.fetchall():
        albums.append({
          "id": row[0],
          "dirpath": row[2]
        })
      
      conn.commit()
      cursor.close()
      
      result = True
    except Exception as e:
      logging.error(e)
      result = False
      
    return albums, result
  
  def delete_album(id: int):
    result = False 
    
    try: 
      conn = Connect().get_connection()

      # Create cursor to perform database operations
      cursor = conn.cursor()

      cursor.execute("DELETE FROM imgdirectories WHERE id = %s", (id,))
      
      conn.commit()
      cursor.close()

      result = True
    except Exception as e:
      logging.error(e)
      result = False
      
    return id, result