""" A module that handles authentication services."""
from ..models.users import User

class AuthService():
    """Manages the authentication service"""
    @staticmethod
    def register_user(data):
        """ Registers a new user """
        user = User(**data)
        user.password = data.get('password')
        user.save()
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        """ Logins a user"""
        user: User = User.find_first_object({'email': email})
        if user and user.is_valid_password(password):
            return user
        return None