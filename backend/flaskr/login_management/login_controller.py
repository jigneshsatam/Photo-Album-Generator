from flask import Flask, Blueprint, Response, jsonify, request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db.postgres_db_connect import Connect
from .login_model import User

login_routes = Blueprint("login_routes", __name__, url_prefix="/users")

@login_routes.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'status': 'JSON data is missing'}), 404

    data = request.get_json()
    username = data.get('userName')
    password = data.get('pwd')

    user_data = User.get_user_by_username(username)

    if user_data and user_data[2] == password:
        token = username + password
        role = 'admin' if user_data[5] == -1 else 'guest'
        response = {
            'status': 'success',
            'message': 'Login successful',
            'id': user_data[0],
            'userName': user_data[1],
            'role': role,
            'token': token
        }
        return make_response(jsonify(response)), 200

    response = {
        'status': 'error',
        'message': 'Invalid username or password'
    }
    return make_response(jsonify(response)), 401




# --------------------------------------------------------------------------------------------

# @login_routes.route('/login', methods=['POST'])
# def login():
#     if not request.is_json:
#         return jsonify({'status': 'JSON data is missing'}), 404

#     data = request.get_json()
#     username = data.get('userName')
#     password = data.get('pwd')

#     user_data = User.get_user_by_username(username)

#     if user_data and user_data[2] == password:
#         token = username + password
#         response = {
#             'status': 'success',
#             'message': 'Login successful',
#             'token': token
#         }
#         return make_response(jsonify(response)), 200

#     response = {
#         'status': 'error',
#         'message': 'Invalid username or password'
#     }
#     return make_response(jsonify(response)), 401






# --------------------------------------------------------------------------------------------

# # Login User call
# @login_routes.route("/login", methods=['POST'])
# def login():
#     # Check if data is provided in request
#     if not request.data:
#         return jsonify({'status': 'JSON data is missing'}), 404

#     # Get username from request
#     if str(request.json.get('userName')) != 'None':
#         user_name = str(request.json.get('userName'))
#     else:
#         return jsonify({'status': 'username is missing'}), 404

#     # Get password from request
#     if str(request.json.get('pwd')) != 'None':
#         password = str(request.json.get('pwd'))
#     else:
#         return jsonify({'status': 'password is missing'}), 404

#     # Get user type from request
#     user_type = str(request.json.get('userType')) if str(request.json.get('userType')) != "None" else "admin"

#     # Get user data from DB
#     user_data = User.get_user_by_username(user_name)

#     if user_data:
#         if check_password_hash(user_data[2], password):
#             return jsonify({'status': 'Login successful for ' + user_data[4] + ', ' + user_data[3],
#                             'userId': user_data[0], 'userType': user_data[5]})
#         else:
#             return jsonify({'status': 'Login failed for ' + user_data[4] + ', ' + user_data[3]}), 401
#     else:
#         return jsonify({'status': 'Login failed for ' + user_name}), 401
