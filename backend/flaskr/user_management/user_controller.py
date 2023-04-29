from flask import Blueprint, Response, jsonify, request
from .user_model import User
from util.error_util import ErrorUtil

users_routes = Blueprint("users_routes", __name__, url_prefix="/users")

# Register User call
@users_routes.route("/RegisterUser", methods=['POST'])
def register_user():
    # Check if data is provided in request
    if not request.data:
        return ErrorUtil.get_json_response(ErrorUtil.JSON_DATA_MISSING)

    # Get username from request
    if str(request.json.get('userName')) != 'None':
        user_name = str(request.json.get('userName'))
    else:
        return ErrorUtil.get_json_response(ErrorUtil.NO_USER_NAME)

    # Get password from request
    if str(request.json.get('pwd')) != 'None':
        password = str(request.json.get('pwd'))
    else:
        return ErrorUtil.get_json_response(ErrorUtil.NO_PASSWORD)

    # Get first name from request
    if str(request.json.get('fName')) != 'None':
        first_name = str(request.json.get('fName'))
    else:
        return ErrorUtil.get_json_response(ErrorUtil.NO_FIRST_NAME)

    # Get last name from request
    if str(request.json.get('lName')) != 'None':
        last_name = str(request.json.get('lName'))
    else:
        return ErrorUtil.get_json_response(ErrorUtil.NO_LAST_NAME)

    # Get user type from request
    user_type = str(request.json.get('userType')) if str(request.json.get('userType')) != "None" else "admin"

    # Create user in DB
    user_id, result = User.create_user(user_name, password, first_name, last_name, user_type)

    if result:
        return jsonify({'status': 'Account has been registered for ' + last_name + ', ' + first_name,
                         'userId': user_id, 'userType': user_type})
    else:
        return jsonify({'status': 'User creation failed for ' + last_name + ', ' + first_name}), 500

@users_routes.route("/login")
def login():
  pass
