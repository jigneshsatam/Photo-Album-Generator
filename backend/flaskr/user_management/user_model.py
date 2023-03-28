import os
import psycopg2

# Connect to database
cnxn = psycopg2.connect("postgresql://photogendocker:photogendocker@database:5432/photogen")

# Create cursor to perform database operations
cursor = cnxn.cursor()

class User:
    def create_user(user_name, password, first_name, last_name, user_type):
        result = False

        try:
            cursor.execute(
            "insert into UserInfo(userName, pwd, firstName, lastName, userType)"
            " values('" + user_name + "', '" + password + "', '" + first_name + "', '" + last_name +
            "', '" + user_type + "')")

            cnxn.commit()

            result = True
        except:
            result = False        

        return result