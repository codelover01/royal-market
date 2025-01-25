""" A module that handles authentication services."""
from models.users import User
from utils.email_validator import is_valid_email


class AuthService():
    """Manages the authentication service"""
    @staticmethod
    def register_user(data):
        """ Registers a new user
        Args:
            - Data: User Registration required data
                - Username
                - email
                - password
                - firstname(Optional)
                - lastname(Optional)
        Returns:
            The registered user after saving to the database.
        """

        # Validate email format
        email = data.get('email')
        if not is_valid_email(email):
            raise ValueError( "Invalid email format")

        # Check if passwords match
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not confirm_password:
            raise ValueError("Confirm passowrd is missing")
        if password != confirm_password:
            raise ValueError("Passwords do not match.")
        
        # Remove 'confirm_password' from the data to 
        # avoid passing it to the User model
        data.pop('confirm_password', None)

        user = User(**data)
        user.password = data.get('password')
        user.save()
        return user
    
    @staticmethod
    def authenticate_user(email, password):
        """ Logins a user
        Args:
            - email: registered user's email
            - password: registered user's password
        Returns:
            - user on successful login
            - None if user is not found.

        """
        user: User = User.find_first_object({'email': email})
        if user and user.is_valid_password(password):
            return user
        return None