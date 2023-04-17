from flaskr.db.postgres_db_connect import Connect
import logging

class User:
    def create_user(user_name, password, first_name, last_name, user_type):
        result = False

        try:
            conn = Connect().get_connection()

            # Create cursor to perform database operations
            cursor = conn.cursor()

            cursor.execute(
            "insert into UserInfo(userName, pwd, firstName, lastName, userType)"
            " values('" + user_name + "', '" + password + "', '" + first_name + "', '" + last_name +
            "', '" + user_type + "')")

            conn.commit()

            cursor.close()

            result = True
        except Exception as e:
            logging.error(e)
            result = False        

        return result