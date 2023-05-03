# from flaskr.db.postgres_db_connect import Connect
# import logging


# class User:
#     @staticmethod
#     def create_user(user_name, password, first_name, last_name, user_type):
#         result = False
#         user_id = None

#         try:
#             conn = Connect().get_connection()

#             # Create cursor to perform database operations
#             cursor = conn.cursor()

#             cursor.execute(
#                 "insert into UserInfo(userName, pwd, firstName, lastName, userType)"
#                 " values(%s, %s, %s, %s, %s) returning id",
#                 (user_name, password, first_name, last_name, user_type)
#             )

#             # Get id for new directory path
#             user_id = int(cursor.fetchone()[0])

#             conn.commit()

#             cursor.close()

#             result = True
#         except Exception as e:
#             logging.error(e)
#             result = False

#         return user_id, result
    
    
#     @staticmethod
#     def get_user_by_username(username):
#         try:
#             conn = Connect().get_connection()
#             cursor = conn.cursor()

#             cursor.execute(
#                 f"SELECT * FROM UserInfo WHERE userName='{username}'"
#             )

#             user_data = cursor.fetchone()

#             cursor.close()
#             conn.close()

#             return user_data
#         except Exception as e:
#             logging.error(e)
#             return None

from flaskr.db.postgres_db_connect import Connect
import logging


class User:
    @staticmethod
    def create_user(user_name, password, first_name, last_name, user_type):
        user_id = None

        try:
            with Connect().get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO UserInfo(userName, pwd, firstName, lastName, userType)"
                        " VALUES(%s, %s, %s, %s, %s) RETURNING id",
                        (user_name, password, first_name, last_name, user_type)
                    )

                    # Get id for new directory path
                    user_id = int(cursor.fetchone()[0])

                    conn.commit()
        except Exception as e:
            logging.error(e)
            return user_id, False

        return user_id, True

    @staticmethod
    def get_user_by_username(username):
        try:
            with Connect().get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM UserInfo WHERE userName=%s",
                        (username,)
                    )

                    user_data = cursor.fetchone()

            return user_data
        except Exception as e:
            logging.error(e)
            return None