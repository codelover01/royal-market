"""
A module that carries out all the apps related authentication processes.
"""

import logging

logging.basicConfig(level=logging.DEBUG)
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity
    )
from services.authService import AuthService
from models.users import User
from utils.email_utils import send_password_reset_email, send_verification_email

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register/', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """ Registers a new user
    Args:
        - Data: User Registration required data
                - Username
                - email
                - password
                - firstname(Optional)
                - lastname(Optional)
    Returns:
        - JSON responses and their status codes
        - Jsonifies the successfully registered user with 201 status code
    """
    # Debug CSRF Tokens
    csrf_header = request.headers.get('X-CSRFToken')
    csrf_cookie = request.cookies.get('csrf_token')
    logging.debug(f"CSRF Header Token: {csrf_header}")
    logging.debug(f"CSRF Cookie Token: {csrf_cookie}")

    data = request.get_json()
    logging.debug(f"Received data: {data}")
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    try:
        user = AuthService.register_user(data)
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_json()
            }), 201
    
    except ValueError as e:
        logging.error(f"ValueError: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.exception("Unexpected error occurred during registration")
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ Logins a user 
    Args:
        email(str): User's email
        password(str): User's password

    Returns:
        JSON responses and their status codes
        200 : When the user is successfully logged in
        400 : For Invalid JSON and missing (email and password)
        401 : Invalid Email and password
        500 : Any other exceptions
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({
                'error': 'Email and password required.'
                }), 400
        
        user = AuthService.authenticate_user(email, password)
        if user:
            access_token = create_access_token(identity=user.username)
            
            # Create the refresh token
            refresh_token = create_refresh_token(identity=user.username)

            # Create response object
            response = make_response(jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'refresh_token': refresh_token
            }), 200)
            
            # Set the refresh token as an HTP-only cookie
            response.set_cookie(
                'refresh_token', refresh_token, httponly=False,
                secure=True, samesite='Lax', max_age=604800
                )
            
            response.set_cookie(
                'access_token', access_token, httponly=False,
                secure=True, samesite='Lax', max_age=604800
                )
            
            # Return access token in response body
            response.json['access_token'] = access_token
            return response
        return jsonify({
            'error': 'Invalid email or password'
        }), 401
    except Exception as e:
        return jsonify(
            {
                'error': 'An error ocurred during the login',
                'error_info': str(e)
                }), 500


@auth_bp.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    """ Logs the current user out."""
    return jsonify({"message": "Logout successful"}), 200

@auth_bp.route('/refresh', methods=['POST'], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    """ Refresh the access token using thhe refresh token stored in cookie """
    # Get current user from the refresh token
    current_user = get_jwt_identity()

    # Create a new access token
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200

@auth_bp.route('/request-password-reset', methods=['GET','POST'], strict_slashes=False)
def request_password_reset():
    """ Requests for a password reset
    Args:
        email: user's email
    Return:
        - Password reset email.
    """
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({
            "message": "Email is required"
        }), 400
    
    user: User = User.find_first_object(email = email)
    if user:
        send_password_reset_email(user)
    return jsonify({
        "message": "Check your email, a password reset email has been sent"
    }), 200


@auth_bp.route('/password-reset/<token>', methods=['GET', 'POST'], strict_slashes = True)
def password_reset_token(token):
    """ Resets the password
    Args:
        Token: password reset token
        new_password: user's new password
    Returns:
        A Password reset token
        A new set password.
    """
    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({
            "message": " Password is required."
        }), 400
    
    user: User = User.verify_password_reset_token(token)
    if not user:
        return jsonify({
            "message": " Invalid or expired token"
        }), 400
    
    user.password = new_password
    user.save()

    return jsonify({
        "message": "Password has been reset successfully."
        }), 200

@auth_bp.route('/request-verify-email', methods = ['GET', 'POST'], strict_slashes = False)
def request_verify_email():
    """ Verifies the validity of an email
    Args:
        email: Email to verify
    Return:
        Email verification email.
    """
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({
            "message": "Email is required."
        }), 400
    
    user: User = User.find_first_object(email = email)
    if user:
        send_verification_email(user)
    return jsonify({
        "message": "Check your email, a verification link has been sent."
    }), 200


@auth_bp.route('/verify-email/<token>', methods=['GET', 'POST'], strict_slashes = False)
def verify_email(token):
    """ Verifies the email
    Args:
        token: email verification token
    Return:
        Saves the user's email to database.
    """
    user: User = User.verify_email_token(token)
    if not user:
        return jsonify({
            "message": "Invalid or expired token."
        }), 400
    
    if user.email_verified:
        return jsonify({
            "message": "Email already verified."
            }), 200
    
    
    user.email_verified = True
    user.save()

    return jsonify({
        "message": "Email has been verified successfully."
    }), 200