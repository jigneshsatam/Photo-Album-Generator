from flaskr.db.postgres_db_connect import Connect
import logging

class User:
    def create_user(user_name, password, first_name, last_name, admin_id):
        result = False

        conn = Connect().get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("insert into UserInfo(userName, pwd, firstName, lastName, admin_id)"
                           " values('" + user_name + "', '" + password + "', '" + first_name + "', '" + last_name +
                           "', " + str(admin_id) + ") returning id")

            # Get id for new user
            user_id = int(cursor.fetchone()[0])

            conn.commit()            

            result = True

        except Exception as e:
            logging.error(e)
            result = False

        finally:
            cursor.close()        

        return user_id, result