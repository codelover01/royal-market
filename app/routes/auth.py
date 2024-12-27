"""
A module that carries out all the apps related authentication processes.
"""
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from ..services.authService import AuthService
from ..models.users import User
from ..utils.email_utils import send_password_reset_email, send_verification_email

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register/', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """ Registers a new user"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    try:
        user = AuthService.register_user(data)
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_json()
            }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """ Logins a user """
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
        login_user(user)  # Logs in the user and sets session
        return jsonify({
            'message': 'Login successfully',
            'user': user.to_json()
            }), 200
    return jsonify({'error': 'Invalid email or password'}), 401


@auth_bp.route('/logout', methods=['POST'], strict_slashes=False)
@login_required
def logout():
    """ Logs the current user out."""
    logout_user()  # Logs out the current user
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route('/password-reset-request', methods=['GET','POST'], strict_slashes=False)
def password_reset_request():
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

@auth_bp.route('/verify-email-request', methods = ['GET', 'POST'], strict_slashes = False)
def verify_email_request():
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