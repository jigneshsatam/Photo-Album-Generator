import os
import random
from flaskr.db.postgres_db_connect import Connect
import logging
from psycopg2.extras import RealDictCursor


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

  @classmethod
  def get_iamges_with_tags(cls, dir_id: int):
    images_with_tags_dict = {}

    try:
      conn = Connect().get_connection()

      # Create cursor to perform database operations
      cursor = conn.cursor(cursor_factory=RealDictCursor)

      # Insert new directory path
      query = f"""
        select
          photo_id, photo_path, tag.tag_id as tag_id, tag.tag as name
        from
            photo
          left join
            tagging
          on tagging.img_id = photo.photo_id
          left join
            tag
          on tagging.tag_id = tag.tag_id
        where
          photo_directory = {dir_id};
      """
      logging.debug(query)
      cursor.execute(query)

      # Get id for new directory path
      if cursor.pgresult_ptr is not None:
        for row in cursor.fetchall():
          img_obj = images_with_tags_dict.get(
              row["photo_id"],
              {"photo_id": row["photo_id"], "path": row["photo_path"], "tags": []})
          if row["tag_id"] is not None:
            tag = {"tag_id": row["tag_id"], "name": row["name"]}
            tags = img_obj.get("tags")
            tags.append(tag)
            img_obj["tags"] = tags
          images_with_tags_dict[row["photo_id"]] = img_obj

    except Exception as e:
      logging.error("Error:: Fetching images along with tags ==> ", e)

    finally:
      # conn.close()
      cursor.close()

    return list(images_with_tags_dict.values())

  def add_new_directory(user_id, dir_path):
    # logging.warning('Start add new directory function')
    result = False
    dir_id = -1

    try:
      conn = Connect().get_connection()

      # Create cursor to perform database operations
      cursor = conn.cursor()

      # Insert new directory path
      query = "insert into imgdirectories(userid, dirpath) values(" + str(
          user_id) + ", '" + dir_path + "') returning id"
      # logging.warning(query)
      cursor.execute(query)

      # Get id for new directory path
      dir_id = int(cursor.fetchone()[0])

      conn.commit()

      # conn.close()
      cursor.close()

      result = True
    except Exception as e:
      logging.error(e)
      result = False

    return dir_id, result

  def add_images(dir_id, dir_path):
    result = False
    img_paths = []

    try:
      conn = Connect().get_connection()

      # Get images in directory path
      for img in os.scandir('uploads/' + dir_path):
        if img.name.endswith(".png") or img.name.endswith(".jpg") or img.name.endswith(".jpeg"):
          img_paths.append(img.path)

      # if dir_path != "":
      #   dir_path = dir_path + '/'

      # Add directory images into photo table
      if len(img_paths) > 0:
        for path in img_paths:
          cursor = conn.cursor()
          insert_query = "insert into photo(photo_directory, photo_path) values(" + str(
              dir_id) + ", '" + str(path) + "')"
          cursor.execute(insert_query)
          conn.commit()

      result = True
    except Exception as e:
      logging.error(e)
      result = False
    finally:
      cursor.close()

    return result

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

  def get_images_from_tags(user_id, tag_list):
    try:
      conn = Connect().get_connection()
      result = []

      # Create cursor to perform database operations
      cursor = conn.cursor()

      # Insert new directory path
      tag_list_string = ', '.join(tag_list)
      query = "select tagging.img_id, photo.photo_path, imgdirectories.dirpath from userinfo inner join imgdirectories on imgdirectories.userid = userinfo.id inner join photo on photo.photo_directory = imgdirectories.id inner join tagging on tagging.img_id = photo.photo_id where tagging.tag_id in (" + tag_list_string + ") and userinfo.id = " + str(
          user_id)
      # logging.warn(query)
      cursor.execute(query)

      # Store result in dictionary object
      for row in cursor.fetchall():
        result.append({
            "imageId": row[0],
            "imagePath": row[1],
            "directoryPath": row[2]
        })

      conn.commit()
      cursor.close()

    except Exception as e:
      logging.error(e)

    return result
