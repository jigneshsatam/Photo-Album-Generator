from flaskr.db.postgres_db_connect import Connect
import logging

class User:
    def create_user(user_name, password, first_name, last_name, admin_id):
        result = False

        try:
            conn = Connect().get_connection()

            # Create cursor to perform database operations
            cursor = conn.cursor()

            cursor.execute("insert into UserInfo(userName, pwd, firstName, lastName, admin_id)"
                           " values('" + user_name + "', '" + password + "', '" + first_name + "', '" + last_name +
                           "', " + str(admin_id) + ") returning id")

            # Get id for new directory path
            user_id = int(cursor.fetchone()[0])

            conn.commit()

            cursor.close()

            result = True
        except Exception as e:
            logging.error(e)
            result = False        

        return user_id, result