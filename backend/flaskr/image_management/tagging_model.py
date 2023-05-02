from flaskr.db.postgres_db_connect import Connect


# def parse_tags(arr):
#     for a in array:
#         if a == "null":
#            unlisted_tags =[]

#     pass

class Taging:

    def __init__(self, tag_id, img_id) -> None:
        self.tag_id = tag_id
        self.img_id = img_id

    @classmethod
    def tag_image(cs, img_id, tag):

        add_tag_query = f'INSERT INTO tagging (tag_id, img_id) VALUES("{tag_id}","{img_id}");'
        tag_in_db =[]
        #tag_with_id =[]
        tag_names =[]
        new_tag_names =[]
        new_tag_ids = []
        tag_with_ids = []
        tagging_ids=[]



        try:
            conn = Connect().get_connection()
            cursor = conn.cursor()
            #Check for existing tags in datbase compare to what request is sending
            # get all the names a.k.a string values from request
            for t in tag:
                tag_names.append(f"'{t.get('name')}'")

            # get the tag_id colum, and tag(name) column  from tag table
            query_get_id = f'SELECT min(tag_id), tag from tag WHERE tag in ({",".join(tag_names)}) GROUP BY tag;'
            print(query_get_id)
            cursor.execute(query_get_id)

            existing_tags = {}
            if cursor.pgresult_ptr is not None:
                for row in cursor.fetchall():
                    existing_tags[row[1]] = row[0]

            for t in tag:
                tag_id = existing_tags.get(tag.get("name"), None)
                if tag_id is None:
                    new_tag_names.append(f"( '{tag.get('name')}' )")
                else:
                    tag_in_db.append(tag_id)

            # Insert new tags in the tag table of the database and get the IDs
            new_tags_query = f"insert into tag(tag) values( {', '.join(new_tag_names) } ) RETURNING tag_id;"

            if new_tag_names:
                print(new_tags_query)
                cursor.execute(new_tags_query)

                if cursor.pgresult_ptr is not None:
                    for row in cursor.fetchall():
                        new_tag_ids.append(row[0])

                conn.commit()
                print(new_tag_ids)
            #new tags with new id
            tag_with_ids.extend(new_tag_ids)


            # # QUERY the photos table to see if the photo exist
            # photo_query = f"SELECT * FROM photos WHERE photo_id = {img_id}; "
            values_for_insertion = []

            for tag_id in tag_with_ids:
                    values_for_insertion.append(f"( {img_id}, {tag_id} )")

            tagging_query = f'INSERT into tagging(img_id, tag_id) Values {",".join(values_for_insertion)} ON CONFLICT DO NOTHING returning tagging_id; '




            if values_for_insertion:
                print(tagging_query)
                cursor.execute(tagging_query)

                if cursor.pgresult_ptr is not None:
                    for row in cursor.fetchall():
                        tagging_ids.append(row[0])


                conn.commit()
                print(new_tag_ids)
            print(f"Tag: {tag_id} added to photo: {img_id}")
        except Exception as e:
            print(e)
            print(f'Addition of tag: {tag_id} to photo:{img_id} failed')

        finally:
            cursor.close

        return tagging_ids


    @classmethod
    def get_taged_img(cs, tag_id, img_id):

        tagged_query = f'SELECT tag_id, img_id FROM tagging WHERE tag_id = {tag_id} AND img_id = {img_id};'

        try:
            conn = Connect().get_connection()

            # Create cursor to perform database operations
            cursor = conn.cursor()
            # cursor = db_temp_connection()
            print(tagged_query)

            cursor.execute(tagged_query)
            #query_df = pd.DataFrame(cursor.fetchall())
            tagging = []
            #cursor.execute(query)
            for row in cursor.fetchall():
                tagging.append({"tag_id" : row[0],
                                  "img_id": row[1]
                                  })
            cursor.close()
            return tagging


        except Exception as e:
            print(e)
            print(f"no image:{img_id} with tag:{tag_id} ")

        # return query_df
        finally:
            cursor.close()

    # tag all images in a directory
    @classmethod
    def tag_all_images(cs, dir_id, tags):
        img_ids = []
        tag_ids = []

        # Present in the database
        tag_with_ids = []

        # New tags  i.e tags without id
        # new_tag_names = [('tag_new'), ('tag_new_2')]
        new_tag_names = []
        new_tag_ids = []

        # tag_names = ["'tag_new'", "'tag_new_2'"]
        tag_names = []

        tagging_ids= []

        try:
            # Create cursor to perform database operations
            conn = Connect().get_connection()
            cursor = conn.cursor()

            #get the string portion of the tag {'name': 'string'}
            for tag in tags:
                tag_names.append(f"'{tag.get('name')}'")

            # get the tag_id colum, and tag(name) column  from tag table
            query_get_id = f'SELECT min(tag_id), tag from tag WHERE tag in ({",".join(tag_names)}) GROUP BY tag;'

            print(query_get_id)
            cursor.execute(query_get_id)

            # existing_tag_ids = []
            existing_tags = {}

            if cursor.pgresult_ptr is not None:
                for row in cursor.fetchall():
                    existing_tags[row[1]] = row[0]
                    # existing_tag_ids.append(row[0])
                    # existing_tag_names.append(row[1])

            for tag in tags:
                tag_id = existing_tags.get(tag.get("name"), None)
                if tag_id is None:
                    new_tag_names.append(f"( '{tag.get('name')}' )")
                else:
                    tag_with_ids.append(tag_id)

            # Insert new tags in the tag table of the database and get the IDs
            new_tags_query = f"insert into tag(tag) values( {', '.join(new_tag_names) } ) RETURNING tag_id;"

            # for image
            img_ids_query = f'SELECT photo_id FROM photo inner join imgdirectories on imgdirectories.id = photo.photo_id WHERE imgdirectories.id = {dir_id};'


            # ============== Tagging Start ======================

            if new_tag_names:
                print(new_tags_query)
                cursor.execute(new_tags_query)

                if cursor.pgresult_ptr is not None:
                    for row in cursor.fetchall():
                        new_tag_ids.append(row[0])

                conn.commit()
                print(new_tag_ids)

            tag_with_ids.extend(new_tag_ids)


            # ============== Tags ======================


            # ============== Images Start ======================

            print(img_ids_query)
            cursor.execute(img_ids_query)
            img_ids = []
            #cursor.execute(query)
            if cursor.pgresult_ptr is not None:
                for row in cursor.fetchall():
                    img_ids.append(row[0])

            # return img_ids
            # ============== Images ======================

            values = []

            for img_id in img_ids:
                for tag_id in tag_with_ids:
                    values.append(f"( {img_id}, {tag_id} )")



            tagging_query = f'insert into tagging(img_id, tag_id) Values {",".join(values)} ON CONFLICT DO NOTHING returning tagging_id; '

            if values:
                print(tagging_query)
                cursor.execute(tagging_query)

                if cursor.pgresult_ptr is not None:
                    for row in cursor.fetchall():
                        tagging_ids.append(row[0])


                conn.commit()
                print(new_tag_ids)


        except Exception as e:
            print("Error::", e)
            print(f"no image:{dir_id} with tag:{tags} ")

        finally:
            cursor.close

        return tagging_ids

    # delete tag from image --NOTE: per request only 1 tag is removed from 1 image.
    @classmethod
    def delete_tags(cs, tag_id, img_id):
       del_query = f'DELETE FROM tagging WHERE tag_id= {tag_id} AND img_id = {img_id};'


       try:
           conn = Connect().get_connection()
           cursor = conn.cursor()
           cursor.execute(del_query)
           cursor.close()
           print('Tag Deleted')

       except Exception as e:
                 print(e)
                 print("no tag exist")

       finally:
           cursor.close()