from flask import Blueprint, Response, jsonify, request
from .user_model import User

users_routes = Blueprint("users_routes", __name__, url_prefix="/users")

# Register User call
@users_routes.route("/RegisterUser", methods=['POST'])
def register_user():
    # Check if data is provided in request
    if not request.data:
        return jsonify({'status': 'JSON data is missing'}), 404

    # Get username from request
    if str(request.json.get('userId')) != 'None':
        user_name = str(request.json.get('userId'))
    else:
        return jsonify({'status': 'username is missing'}), 404

    # Get password from request
    if str(request.json.get('pwd')) != 'None':
        password = str(request.json.get('pwd'))
    else:
        return jsonify({'status': 'password is missing'}), 404

    # Get first name from request
    if str(request.json.get('fName')) != 'None':
        first_name = str(request.json.get('fName'))
    else:
        return jsonify({'status': 'first name is missing'}), 404

    # Get last name from request
    if str(request.json.get('lName')) != 'None':
        last_name = str(request.json.get('lName'))
    else:
        return jsonify({'status': 'last name is missing'}), 404

    # Get user type from request
    user_type = str(request.json.get('userType')) if str(request.json.get('userType')) != "None" else "admin"

    # Create user in DB
    result = User.create_user(user_name, password, first_name, last_name, user_type)

    if result:
        return jsonify({'status': 'Account has been registered for ' + last_name + ', ' + first_name})
    else:
        return jsonify({'status': 'User creation failed for ' + last_name + ', ' + first_name}), 500

@users_routes.route("/login")
def login():
  pass
