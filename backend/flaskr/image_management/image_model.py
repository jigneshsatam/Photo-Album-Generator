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

    conn = Connect().get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
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
          photo_directory = {dir_id}
        order by photo_id, tag.tag_id;
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
      cursor.close()

    return list(images_with_tags_dict.values())

  def add_new_directory(user_id, dir_path):
    result = False
    dir_id = -1

    conn = Connect().get_connection()
    cursor = conn.cursor()

    try:
      # Insert new directory path
      query = "insert into imgdirectories(userid, dirpath) values(" + str(
          user_id) + ", '" + dir_path + "') returning id"
      cursor.execute(query)

      # Get id for new directory path
      dir_id = int(cursor.fetchone()[0])

      conn.commit()

      result = True

    except Exception as e:
      logging.error(e)
      result = False

    finally:
      cursor.close()

    return dir_id, result

  def add_images(dir_id, dir_path):
    result = False
    img_paths = []

    conn = Connect().get_connection()
    cursor = conn.cursor()

    try:
      # Get images in directory path
      for img in os.scandir('uploads/' + dir_path):
        if img.name.endswith(".png") or img.name.endswith(".jpg") or img.name.endswith(".jpeg"):
          img_paths.append(img.path)

      # Add directory images into photo table
      if len(img_paths) > 0:
        for path in img_paths:
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

    conn = Connect().get_connection()
    cursor = conn.cursor()

    try:
      query = "SELECT * FROM imgdirectories"

      cursor.execute(query)

      for row in cursor.fetchall():
        albums.append({
            "id": row[0],
            "dirpath": row[2]
        })

      conn.commit()

      result = True

    except Exception as e:
      logging.error(e)
      result = False

    finally:
      cursor.close()

    return albums, result

  def delete_album(id: int):
    result = False

    conn = Connect().get_connection()
    cursor = conn.cursor()

    try:
      cursor.execute("DELETE FROM imgdirectories WHERE id = %s", (id,))

      conn.commit()

      result = True

    except Exception as e:
      logging.error(e)
      result = False

    finally:
      cursor.close()

    return id, result

  def get_images_from_tags(user_id, tag_list):

    conn = Connect().get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
      # Insert new directory path
      tag_list_string = ', '.join(tag_list)

      # tag_list_string = ""
      # for tag_id in tag_list:
      #   tag_list_string += f' tagging.tag_id = {tag_id} AND '
      # tag_list_string = tag_list_string.rstrip("AND ")

      query = f"""
        select
          tagging.img_id as img_id, photo.photo_path as photo_path, tag.tag_id as tag_id, tag.tag as name
        from
            tag
          left join
            tagging
          on tagging.tag_id = tag.tag_id
          left join
            photo
          on tagging.img_id = photo.photo_id
          left join
            imgdirectories
          on photo.photo_directory = imgdirectories.id
        where
          imgdirectories.userid = {user_id}
        AND
          tagging.img_id IN (
          SELECT img_id
          FROM tagging
          WHERE tagging.tag_id IN ({tag_list_string})
          GROUP BY tagging.img_id
          HAVING COUNT(DISTINCT tag_id) = {len(tag_list)}
        );

      """

      # query = "select tagging.img_id, photo.photo_path, imgdirectories.dirpath from  imgdirectories on imgdirectories.userid = userinfo.id inner join photo on photo.photo_directory = imgdirectories.id inner join tagging on tagging.img_id = photo.photo_id where tagging.tag_id in (" + tag_list_string + ") and userinfo.id = " + str(
      #     user_id)
      print(query)
      cursor.execute(query)

      images_with_tags_dict = {}

      # Store result in dictionary object
      if cursor.pgresult_ptr is not None:
        for row in cursor.fetchall():
          img_obj = images_with_tags_dict.get(
              row["img_id"],
              {"imageId": row["img_id"], "imagePath": row["photo_path"], "tags": []})
          if row["tag_id"] is not None:
            tag = {"tag_id": row["tag_id"], "name": row["name"]}
            tags = img_obj.get("tags")
            tags.append(tag)
            img_obj["tags"] = tags
          images_with_tags_dict[row["img_id"]] = img_obj

      # for row in cursor.fetchall():
      #   if not any(d['imageId'] == row[0] for d in result):
      #     result.append({
      #         "imageId": row[0],
      #         "imagePath": row[1],
      #         "directoryPath": row[2]
      #     })

      # conn.commit()

      # # Get tags for each image in image list
      # for dictionary in result:
      #   tags = []
      #   tags_query = "select tag.tag_id, tag.tag from tag inner join tagging on tagging.tag_id = tag.tag_id where tagging.img_id = " + \
      #       str(dictionary['imageId'])
      #   cursor.execute(tags_query)
      #   for row in cursor.fetchall():
      #     tags.append({
      #         "tag_id": row[0],
      #         "name": row[1]
      #     })
      #   conn.commit()
      #   dictionary.update({"tags": tags})

    except Exception as e:
      logging.error(e)

    finally:
      cursor.close()

    return list(images_with_tags_dict.values())
