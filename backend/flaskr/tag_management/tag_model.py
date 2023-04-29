from flaskr.db.postgres_db_connect import Connect
import logging

class Tag:
    def create_tag(tags):
        result = False

        try:
            conn = Connect().get_connection()
           
            cursor = conn.cursor()

            # for tag in tags:
            #     cursor.execute(
            #     "select * from tag"
            #     "  where name = ' " + tag + " ' ")
            #     print(tag)

            def stringify(v): 
                return "('%s')" % (v)

            #transform all to string
            v = map(stringify, tags)

            #glue them together
            batchData = ", ".join(e for e in v)

            # sql = "INSERT INTO tag (tag) \
            # VALUES %s" % batchData 
            # "ON CONFLICT (tag) DO NOTHING"
            
            sql = "INSERT INTO tag (tag) \
                  VALUES %s \
                  ON CONFLICT (tag) DO NOTHING" % batchData
            
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

            cursor.close()

            result = True
        except Exception as e:
            logging.error(e)
            result = True        

        return 1, result
    
    def get_tags():
        result = False
        tags = []
        try:
            conn = Connect().get_connection()

            #Create cursor to perform database operations
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