from flask import Blueprint, Response, jsonify, request
from .user_model import User
from flask import url_for, Flask, redirect, session
from flask_cors import CORS
import logging
#from flask_mail import Mail, Message

users_routes = Blueprint("users_routes", __name__, url_prefix="/users")

# Register User call
@users_routes.route("/RegisterUser", methods=['POST'])
def register_user():
    # Check if data is provided in request
    if not request.data:
        return jsonify({'status': 'JSON data is missing'}), 404

    # Get username from request
    if str(request.json.get('userName')) != 'None':
        user_name = str(request.json.get('userName'))
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
    
    # Get email from request
    if str(request.json.get('email')) != 'None':
        email = str(request.json.get('email'))
    else:
        return jsonify({'status': 'email is missing'}), 404

    # Get user type from request
    user_type = str(request.json.get('userType')) if str(request.json.get('userType')) != "None" else "admin"

    # Create user in DB
    user_id, result = User.create_user(user_name, password, first_name, last_name, user_type, email)

    if result:
        return jsonify({'status': 'Account has been registered for ' + last_name + ', ' + first_name,
                         'userId': user_id, 'userType': user_type})
    else:
        return jsonify({'status': 'User creation failed for ' + last_name + ', ' + first_name}), 500
    
# login function that uses the userinfo table to verify user credentials
@users_routes.route("/login", methods=['POST'])
def login():
    # Check if data is provided in request
    if not request.data:
        return jsonify({'status': 'JSON data is missing'}), 404

    # Get username from request
    if str(request.json.get('userName')) != 'None':
        user_name = str(request.json.get('userName'))
    else:
        return jsonify({'status': 'username is missing'}), 404

    # Get password from request
    if str(request.json.get('pwd')) != 'None':
        password = str(request.json.get('pwd'))
    else:
        return jsonify({'status': 'password is missing'}), 404

    # Authenticate user
    user = User.authenticate_user(user_name, password)
    if user:
        return jsonify({'status': 'Logged in successfully',
                         'userId': user.id, 'userType': user.user_type})
    else:
        return jsonify({'status': 'Invalid credentials'}), 401
    
    
# reset_password function that uses the password_reset_tokens table to create and verify reset tokens
@users_routes.route("/reset_password", methods=['POST'])
def reset_password():
    # Check if data is provided in request
    if not request.data:
        return jsonify({'status': 'JSON data is missing'}), 404

    # Get email from request
    if str(request.json.get('email')) != 'None':
        email = str(request.json.get('email'))
    else:
        return jsonify({'status': 'email is missing'}), 404

    # Check if user with email exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'status': 'Invalid email'}), 404

    # Generate reset token and save to database
    token = User.generate_password_reset_token(user.id)
    if not token:
        return jsonify({'status': 'Failed to generate reset token'}), 500

    # Send reset password email
    send_password_reset_email(user.email, token)

    return jsonify({'status': 'Password reset email sent to ' + user.email})



# from flask import current_app

# # Initialize Mail
# mail = Mail()

# def send_password_reset_email(user_email, token):
#     # Create a message object
#     msg = Message('Password Reset Request', sender=current_app.config['MAIL_USERNAME'], recipients=[user_email])

#     # Set the message body
#     msg.body = f'''To reset your password, please visit the following link:
# {url_for('reset_password', token=token, _external=True)}

# If you did not make this request, simply ignore this email and no changes will be made.

# Thanks,
# MyApp Team
#     '''

#     # Send the message
#     mail.send(msg)