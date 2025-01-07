# services/wishlist_service.py
from models.wishlist import Wishlist
from models import db

class WishlistService:
    @staticmethod
    def add_to_wishlist(user_id, product_id=None, service_id=None):
        """Add a product or service to the user's wishlist."""
        if product_id:
            existing_item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
            if existing_item:
                return existing_item  # Item already exists in the wishlist
            item = Wishlist(user_id=user_id, product_id=product_id)
            db.session.add(item)
            db.session.commit()
            return item
        elif service_id:
            existing_item = Wishlist.query.filter_by(user_id=user_id, service_id=service_id).first()
            if existing_item:
                return existing_item  # Item already exists in the wishlist
            item = Wishlist(user_id=user_id, service_id=service_id)
            db.session.add(item)
            db.session.commit()
            return item
        return None

    @staticmethod
    def remove_from_wishlist(user_id, product_id=None, service_id=None):
        """Remove a product or service from the user's wishlist."""
        if product_id:
            item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
            return item
        elif service_id:
            item = Wishlist.query.filter_by(user_id=user_id, service_id=service_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
            return item
        return None

    @staticmethod
    def find_by_user(user_id):
        """Fetch all items in a user's wishlist."""
        return Wishlist.query.filter_by(user_id=user_id).all()

