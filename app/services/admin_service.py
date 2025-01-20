from models.users import User

class AdminService:
    """
    Class representation of Admin Service
    """
    @staticmethod
    def get_all_users():
        """Returns all users in the system"""
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Fetches user details by ID"""
        return User.query.get_or_404(user_id)

    @staticmethod
    def get_user_orders(user_id):
        """Fetches all orders for a user"""
        user:User = User.query.get_or_404(user_id)
        return user.orders

    @staticmethod
    def update_user_role(user_id, new_role):
        """Updates user role"""
        user:User = User.query.get_or_404(user_id)
        user.role = new_role
        user.save()  # Save the user object
        return user

    @staticmethod
    def delete_user(user_id):
        """Deletes a user from the database"""
        user:User = User.query.get_or_404(user_id)
        user.delete()
        return {'message': f'User with ID {user_id} has been deleted.'}
