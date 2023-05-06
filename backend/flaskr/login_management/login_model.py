from flaskr.db.postgres_db_connect import Connect
import logging

class User:
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




# --------------------------------------------------------------------------------------------


# class User:
#     @staticmethod
#     def get_user_by_username(username):
#         try:
#             with Connect().get_connection() as conn:
#                 with conn.cursor() as cursor:
#                     cursor.execute(
#                         "SELECT * FROM UserInfo WHERE userName=%s",
#                         (username,)
#                     )

#                     user_data = cursor.fetchone()

#             return user_data
#         except Exception as e:
#             logging.error(e)
#             return None