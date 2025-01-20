# user_service.py
from models.users import User  # Import your User model (assuming SQLAlchemy is used)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.orders import Order
from models.cart import Cart


class UserService:
    """ A Class representation of UserService """
    @staticmethod
    def create_user(username, email, password):
        """
        Create a new user in the database.
        Args:
            - username (str): The username of the new user.
            - email (str): The email address of the new user.
            - password (str): The user's password.
        Returns:
            - User instance: The newly created user.
        """
        # Hash the password before saving
        hashed_password = generate_password_hash(password)
        
        # Create the new user
        user = User(username=username, email=email, password=hashed_password)
        
        # Add the user to the database
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error creating user: {str(e)}")
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        Args:
            - user_id (int): The ID of the user to retrieve.
        Returns:
            - User instance: The user with the given ID.
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user

    @staticmethod
    def get_user_by_username(username):
        """
        Retrieve a user by their username.
        Args:
            - username (str): The username of the user to retrieve.
        Returns:
            - User instance: The user with the given username.
        """
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValueError(f"User with username {username} not found.")
        return user
    
    @staticmethod
    def get_user_orders(user_id):
        """Fetch orders for the user"""
        orders = Order.query.filter_by(user_id=user_id).all()
        return orders
    
    @staticmethod
    def get_user_cart(user_id):
        """Fetch the user's current cart details"""
        cart = Cart.query.filter_by(user_id=user_id, status='active').all()  # Assuming 'active' indicates an ongoing cart
        return cart

    @staticmethod
    def update_user(user_id, username=None, email=None):
        """
        Update an existing user's information.
        Args:
            - user_id (int): The ID of the user to update.
            - username (str, optional): The new username.
            - email (str, optional): The new email.
            - password (str, optional): The new password.
        Returns:
            - User instance: The updated user.
        """
        user = UserService.get_user_by_id(user_id)
        
        if username:
            user.username = username
        if email:
            user.email = email

        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error updating user: {str(e)}")

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user from the database.
        Args:
            - user_id (int): The ID of the user to delete.
        Returns:
            - dict: A success message.
        """
        user = UserService.get_user_by_id(user_id)
        
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User successfully deleted."}
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error deleting user: {str(e)}")
