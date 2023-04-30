from flaskr.db.postgres_db_connect import Connect


def parse_tags(arr):
    for a in array:
        if a == "null":
           unlisted_tags =[]
        
    pass

class Taging:

    def __init__(self, tag_id, img_id) -> None:
        self.tag_id = tag_id
        self.img_id = img_id

    @classmethod
    def add_tags(cs, tag_id, img_id):
        
        add_tag_query = f'INSERT INTO tagging (tag_id, img_id) VALUES("{tag_id}","{img_id}");'
        try:
            conn = Connect().get_connection()
            cursor = conn.cursor()
            cursor.execute(add_tag_query)
            cursor.close()
            print(f"Tag: {tag_id} added to photo: {img_id}")
        except Exception as e:
            print(e)
            print(f'Addition of tag: {tag_id} to photo:{img_id} failed')
   
    @classmethod
    def add_bulk_tags_to_dir(cs, dir_id, tag_id):
        try:
            # need join to obtain photo id from imgdirectories id
            join_photo_imgDir = f'SELECT photo_id FROM (imgdirectories INNER JOIN photo ON id = photo_directory ) WHERE id = {dir_id};'
            conn = Connect().get_connection()
            cursor = conn.cursor()
            cursor.execute(join_photo_imgDir )
            photos_id = []
             
            for row in cursor.fetchall():
                photos_id.append({
                                "img_id" : row[0],
                                  
                                  })
            # append 
            # for id in photos_id:

        
            cursor.close()
            return tagging


            #cursor.execute(query)
            for row in cursor.fetchall():
                photos_id.append(row[0])
             
        
        except Exception as e:
             print(e)
             print('Failed bulk tagging')


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
        
   
    @classmethod
    def create_tagging(cs, dir_id, tags):
        img_ids = []
        tag_ids = []

        # Present in the database
        tag_with_ids = []

        # New tags  i.e tags without id
        # new_tag_names = [('tag_new'), ('tag_new_2')]
        new_tag_names = []
        new_tag_ids = []

        for tag in tags:
            if tag.get("tag_id") == None:
                new_tag_names.append(f"( '{tag.get('name')}' )")
            else:
                tag_with_ids.append(tag.get("tag_id"))
            
        # Insert new tags in the database and get the IDs
        new_tags_query = f"insert into tag(tag) values( {', '.join(new_tag_names) } ) RETURNING tag_id;"


        img_ids_query = f'SELECT photo_id FROM photo inner join imgdirectories on imgdirectories.id = photo.photo_id WHERE imgdirectories.id = {dir_id};'
        
        try:
            # Create cursor to perform database operations
            conn = Connect().get_connection()
            cursor = conn.cursor() 


            # ============== Tags Start ======================
            
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



            tagging_query = f'insert into tagging(img_id, tag_id) Values {",".join(values)} returning tagging_id; '
            tagging_ids= []
            if values:
                print(tagging_query)
                cursor.execute(tagging_query)
                
                if cursor.pgresult_ptr is not None:
                    for row in cursor.fetchall():
                        tagging_ids.append(row[0])
                    

                conn.commit()
                print(new_tag_ids)

            
            
            
            
            
            cursor.close()
            return tagging_ids
    
        
        except Exception as e:
            print(e)
            print(f"no image:{dir_id} with tag:{tags} ")


    
    # def delete_tags(cs, tag_id, img_id):
    #     del_query = f'DELETE FROM taging WHERE tag_id= "{tag_id}", img_id = "{img_id}";'
    #     cursor =db_temp_connection()
    #     try:
    #              cursor.execute(del_query)
    #              cursor.close()
    #              print('Tag Deleted')
        
    #     except Exception as e:
    #              print(e)
    #              print("no tag exist")
       
    #     return " "