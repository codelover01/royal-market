from . import db
from .baseModel import BaseModel

class Wishlist(BaseModel):
    """ Class representation for users' wishlist """
    __tablename__ = 'wishlist'
    
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id',
        name='fk_wishlist_user'
        ),
        nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id',
        name='fk_wishlist_product'
        ),
        nullable=False)
    
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id',
        name='fk_wishlist_service'
        ),
        nullable=False)
    
    product = db.relationship(
        'Product',
        back_populates='wishlist',
        foreign_keys='Wishlist.product_id'
        )
    service = db.relationship(
        'Service',
        back_populates='wishlist',
        foreign_keys='Wishlist.service_id'
        )
    user = db.relationship('User', back_populates='wishlist')

    def __repr__(self):
        return f"<Wishlist {self.id} - User: {self.user_id}, Product: {self.product_id}>"
    
    @classmethod
    def find_by_user(cls, user_id):
        """Fetch all items in a user's wishlist."""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_product(cls, product_id):
        """Fetch all wishlists with a specific product."""
        return cls.query.filter_by(product_id=product_id).all()

    @classmethod
    def find_by_service(cls, service_id):
        """Fetch all wishlists with a specific service."""
        return cls.query.filter_by(service_id=service_id).all()

    @classmethod
    def add_to_wishlist(cls, user_id, product_id=None, service_id=None):
        """Add a product or service to the user's wishlist."""
        if product_id:
            # Add product to wishlist
            existing_item = cls.query.filter_by(user_id=user_id, product_id=product_id).first()
            if existing_item:
                return existing_item  # Item already exists in the wishlist
            item = cls(user_id=user_id, product_id=product_id)
            db.session.add(item)
            db.session.commit()
            return item
        elif service_id:
            # Add service to wishlist
            existing_item = cls.query.filter_by(user_id=user_id, service_id=service_id).first()
            if existing_item:
                return existing_item  # Item already exists in the wishlist
            item = cls(user_id=user_id, service_id=service_id)
            db.session.add(item)
            db.session.commit()
            return item
        return None  # Neither product_id nor service_id was provided

    @classmethod
    def remove_from_wishlist(cls, user_id, product_id=None, service_id=None):
        """Remove a product or service from the user's wishlist."""
        if product_id:
            # Remove product from wishlist
            item = cls.query.filter_by(user_id=user_id, product_id=product_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
            return item
        elif service_id:
            # Remove service from wishlist
            item = cls.query.filter_by(user_id=user_id, service_id=service_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
            return item
        return None  # Neither product_id nor service_id was provided
