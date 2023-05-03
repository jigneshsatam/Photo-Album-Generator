from flask import Flask, Blueprint, Response, jsonify, request, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db.postgres_db_connect import Connect
from .user_model import User

users_routes = Blueprint("users_routes", __name__, url_prefix="/users")


@users_routes.route("/RegisterUser", methods=['POST'])
def register_user():
    if not request.is_json:
        return jsonify({'status': 'JSON data is missing'}), 404

    data = request.get_json()
    user_name = data.get('userName')
    password = data.get('pwd')
    first_name = data.get('fName')
    last_name = data.get('lName')
    user_type = data.get('userType', 'admin')

    missing_fields = []

    if not user_name:
        missing_fields.append('username')
    if not password:
        missing_fields.append('password')
    if not first_name:
        missing_fields.append('first name')
    if not last_name:
        missing_fields.append('last name')

    if missing_fields:
        return jsonify({'status': f"{', '.join(missing_fields)} is missing"}), 404

    user_id, result = User.create_user(user_name, password, first_name, last_name, user_type)

    if result:
        return jsonify({'status': f'Account has been registered for {last_name}, {first_name}',
                         'userId': user_id, 'userType': user_type})
    else:
        return jsonify({'status': f'User creation failed for {last_name}, {first_name}'}), 500


@users_routes.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'status': 'JSON data is missing'}), 404

    data = request.get_json()
    username = data.get('userName')
    password = data.get('pwd')

    user_data = User.get_user_by_username(username)

    if user_data and user_data[2] == password:
        token = username + password
        response = {
            'status': 'success',
            'message': 'Login successful',
            'token': token
        }
        return make_response(jsonify(response)), 200

    response = {
        'status': 'error',
        'message': 'Invalid username or password'
    }
    return make_response(jsonify(response)), 401




# ---------------------------------------------------------------------------------------------

# from flask import Flask, Blueprint, Response, jsonify, request, make_response
# from werkzeug.security import check_password_hash, generate_password_hash
# from flaskr.db.postgres_db_connect import Connect
# from .user_model import User
# # import jwt as jwt

# users_routes = Blueprint("users_routes", __name__, url_prefix="/users")


# @users_routes.route("/RegisterUser", methods=['POST'])
# def register_user():
#     # Check if data is provided in request
#     if not request.data:
#         return jsonify({'status': 'JSON data is missing'}), 404

#     # Get username from request
#     if request.json.get('userName') is not None:
#         user_name = request.json.get('userName')
#     else:
#         return jsonify({'status': 'username is missing'}), 404

#     # Get password from request
#     if request.json.get('pwd') is not None:
#         password = request.json.get('pwd')
#     else:
#         return jsonify({'status': 'password is missing'}), 404

#     # Get first name from request
#     if request.json.get('fName') is not None:
#         first_name = request.json.get('fName')
#     else:
#         return jsonify({'status': 'first name is missing'}), 404

#     # Get last name from request
#     if request.json.get('lName') is not None:
#         last_name = request.json.get('lName')
#     else:
#         return jsonify({'status': 'last name is missing'}), 404

#     # Get user type from request
#     user_type = request.json.get('userType', 'admin')

#     # Create user in DB
#     user_id, result = User.create_user(user_name, password, first_name, last_name, user_type)

#     if result:
#         return jsonify({'status': 'Account has been registered for ' + last_name + ', ' + first_name,
#                          'userId': user_id, 'userType': user_type})
#     else:
#         return jsonify({'status': 'User creation failed for ' + last_name + ', ' + first_name}), 500
    


# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     conn = Connect().get_connection()
    
#     with conn.cursor() as cursor:
#             cursor.execute(
#                 f"SELECT * FROM UserInfo WHERE userName='{username}'"
#             )

#             user_data = cursor.fetchone()

#             if user_data and user_data[2] == password:
#                 token = username + password
#                 response = {
#                     'status': 'success',
#                     'message': 'Login successful',
#                     'token': token
#                 }
#                 return make_response(jsonify(response)), 200

#             response = {
#                 'status': 'error',
#                 'message': 'Invalid username or password'
#             }
#             return make_response(jsonify(response)), 401

# ---------------------------------------------------------------------------------------------

# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     conn = Connect().get_connection()

#     with conn.cursor() as cursor:
#         cursor.execute(
#             f"SELECT * FROM UserInfo WHERE userName='{username}'"
#         )

#         user_data = cursor.fetchone()

#         if user_data and user_data[2] == password:
#             token = jwt.encode({'username': username}, 'secret_key', algorithm='HS256')
#             response = {
#                 'status': 'success',
#                 'message': 'Login successful',
#                 'token': token.decode('utf-8')
#             }
#             return make_response(jsonify(response)), 200

#         response = {
#             'status': 'error',
#             'message': 'Invalid username or password'
#         }
#         return make_response(jsonify(response)), 401




# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     with Connect() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(
#                 f"SELECT * FROM UserInfo WHERE userName='{username}'"
#             )
#             user_data = cursor.fetchone()

#             if user_data and user_data[2] == password:
#                 token = generate_password_hash(username + password)
#                 response = {
#                     'status': 'success',
#                     'message': 'Login successful',
#                     'token': token
#                 }
#                 return make_response(jsonify(response)), 200

#     response = {
#         'status': 'error',
#         'message': 'Invalid username or password'
#     }
#     return make_response(jsonify(response)), 401



# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     conn = Connect().get_connection()

#     try:
#         with conn.cursor() as cursor:
#             cursor.execute(
#                 f"SELECT * FROM UserInfo WHERE userName='{username}'"
#             )

#             user_data = cursor.fetchone()

#             if user_data and user_data[2] == password:
#                 token = username + password
#                 response = {
#                     'status': 'success',
#                     'message': 'Login successful',
#                     'token': token
#                 }
#                 return make_response(jsonify(response)), 200

#             response = {
#                 'status': 'error',
#                 'message': 'Invalid username or password'
#             }
#             return make_response(jsonify(response)), 401

#     finally:
#         conn.close()









# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     conn = Connect().get_connection()
#     cursor = conn.cursor()

#     cursor.execute(
#         f"SELECT * FROM UserInfo WHERE userName='{username}' AND pwd='{password}'"
#     )

#     user_data = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     if user_data:
#         # Note: You might want to use a more secure way of generating the token
#         # instead of concatenating the username and password.
#         token = f"{username}:{password}"
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






# from flaskr.db.postgres_db_connect import Connect

# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     conn = Connect().get_connection()

#     cursor = conn.cursor()

#     cursor.execute(
#         f"SELECT * FROM UserInfo WHERE userName='{username}'"
#     )

#     user_data = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     if user_data and check_password_hash(user_data[2], generate_password_hash(password)):
#         token = generate_password_hash(username + password)
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




# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     conn = Connect().get_connection()

#     cursor = conn.cursor()

#     cursor.execute(
#         f"SELECT * FROM UserInfo WHERE userName='{username}'"
#     )

#     user_data = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     if user_data and check_password_hash(user_data[2], password):
#         token = generate_password_hash(username + password)
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





# @users_routes.route("/login", methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')
#     user_data = User.get_user_by_username(username)

#     return jsonify({'message': 'Login successful.' + "Username:\n" + username + "Password:\n" + password}), 200


# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     user_data = User.get_user_by_username(username)

#     if user_data and check_password_hash(user_data[2], password):
#         token = generate_password_hash(username + password)
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



# @users_routes.route("/", methods=['POST'])
# def login():
#   return jsonify({'message': 'Login successful.'}), 200



# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('pwd')

#     conn = Connect().get_connection()

#     cursor = conn.cursor()

#     cursor.execute(
#         f"SELECT * FROM UserInfo WHERE userName='{username}'"
#     )

#     user_data = cursor.fetchone()

#     cursor.close()
#     conn.close()

#     if user_data and check_password_hash(user_data[2], password):
#         token = generate_password_hash(username + password)
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







# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json.get('userName')
#     password = request.json.get('password')

#     user = User.query.filter_by(username=username).first()

#     if user and check_password_hash(user.password, password):
#         token = user.generate_auth_token()
#         response = {
#             'status': 'success',
#             'message': 'Login successful',
#             'token': token.decode('ascii')
#         }
#         return make_response(jsonify(response)), 200

#     response = {
#         'status': 'error',
#         'message': 'Invalid username or password'
#     }
#     return make_response(jsonify(response)), 401

# users_routes = Blueprint('users', __name__)

# @users_routes.route('/register', methods=['POST'])
# def register():
#     username = request.json['username']
#     email = request.json['email']
#     password = request.json['password']
#     user = User(username=username, email=email)
#     user.set_password(password)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully!'}), 201

# @users_routes.route('/login', methods=['POST'])
# def login():
#     username = request.json['username']
#     password = request.json['password']
#     user = User.query.filter_by(username=username).first()
#     if not user or not user.check_password(password):
#         return make_response(jsonify({'error': 'Invalid username or password'}), 401)
#     token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'your_secret_key')
#     return jsonify({'token': token.decode('UTF-8')})

# @users_routes.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data:
#         return jsonify({'message': 'Invalid request format.'}), 400
    
#     username = data.get('username')
#     password = data.get('password')
#     if not username or not password:
#         return jsonify({'message': 'Missing username or password.'}), 400
    
#     user = User.query.filter_by(username=username).first()
#     if not user or not check_password_hash(user.password, password):
#         return jsonify({'message': 'Invalid username or password.'}), 401
    
#     # TODO: Generate and return a JWT token for the authenticated user
#     return jsonify({'message': 'Login successful.'}), 200




