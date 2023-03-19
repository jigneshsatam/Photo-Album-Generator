from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Connect to database
cnxn = psycopg2.connect(
        database="root",
        user="photogendocker",
        password="photogendocker",
        host="127.0.0.1"
    )

# Create cursor to perform database operations
cursor = cnxn.cursor()


@app.route('/RegisterUser', methods=['POST'])
def register_user():
    # Check if data is provided in request
    if not request.data:
        return jsonify({'status': 'JSON data is missing'}), 404

    # Get username from request
    user_name = str(request.json.get('userId'))

    # Get password from request
    password = str(request.json.get('pwd'))

    # Get first name from request
    first_name = str(request.json.get('fName'))

    # Get last name from request
    last_name = str(request.json.get('lName'))

    # Get user type from request
    user_type = str(request.json.get('userType')) if str(request.json.get('userType')) != "None" else "admin"

    cursor.execute(
        "insert into UserInfo(userName, passWord, firstName, lastName, userType)"
        " values('" + user_name + "', '" + password + "', '" + first_name + "', '" + last_name +
        "', '" + user_type + "')")

    cnxn.commit()

    return jsonify({'status': 'Account has been registered for ' + last_name + ', ' + first_name})


if __name__ == "__main__":
    app.run()
