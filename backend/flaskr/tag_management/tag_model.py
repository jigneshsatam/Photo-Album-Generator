from flaskr.db.postgres_db_connect import Connect
import logging


class Tag:
  tag_id: int = None
  name: str = ""

  def __init__(self, tag_id: int = None, name: str = ""):
    self.tag_id = tag_id
    self.name = name

  def create_tag(tags):
    result = False
    try:
      conn = Connect().get_connection()
      cursor = conn.cursor()
      getTagsQuery = "SELECT tag FROM tag"  # executing in line 14

      # When new tag is added, it checks duplicates and SQL querying to database to get list of tags
      cursor = conn.cursor()
      cursor.execute(getTagsQuery)
      # get all tag names in tagRows variable
      tagRows = cursor.fetchall()
      # when we get data from db, I am restructuring as an array
      tagLists = [entry for entry, in tagRows]
      # defined unique tags array (blank)
      uniqueTags = []
      # running for loop on tag list
      for element in tags:
        # check if tag sent by used is in db or not
        # if tag is not in tag list, then it will push that tag in the unique tags array
        if element not in tagLists:
          # element checks tags one by one
          uniqueTags.append(element)
      # adding for logging purposes
      print('uniqueTags to Insert Are -->>>', uniqueTags)
      print('Tags Sent By User', tags)
      if len(uniqueTags):
        # in a single query, it sends all the data
        # v = string
        def stringify(tagstring):
          return "('%s')" % (tagstring)

        # transform all to string
        # pass down all unique tags in a string format
        tagstring = map(stringify, uniqueTags)
        # glue them together
        batchData = ", ".join(e for e in tagstring)

        print('Batch Query To insert SQL', batchData)
        # Insert Batch Unique Tags Data

        # batch data was generated from stringify function
        sql = "insert into tag (tag) \
                VALUES %s" % batchData
        cursor.execute(sql)
      conn.commit()
      cursor.close()
      result = True
    except Exception as e:
      logging.error(e)
      result = False

    return result

  def get_tags():
    result = False
    tags = []
    try:
      conn = Connect().get_connection()

      # Create cursor to perform database operations
      cursor = conn.cursor()

      query = "SELECT * FROM tag"

      cursor.execute(query)
      for row in cursor.fetchall():
        tags.append({
            "id": row[0],
            "name": row[1]
        })

       #     tags = cursor.fetchall()

      conn.commit()
      cursor.close()

      result = True
    except Exception as e:
      logging.error(e)
      result = False

    return tags, result
