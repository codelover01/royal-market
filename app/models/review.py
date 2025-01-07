from . import db
from datetime import datetime, timezone
from .baseModel import BaseModel

class Review(BaseModel):
    """ A Review class that handles the Reviews made by users"""
    __tablename__ = 'reviews'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # e.g., 1-5
    comment = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    user = db.relationship('User', back_populates='reviews')
    product = db.relationship('Product', back_populates='reviews')
    service = db.relationship('Service', back_populates='reviews')
    business = db.relationship('Business', back_populates='reviews')


    def __repr__(self):
        return f"<Review {self.id} - Product: {self.product_id}, Rating: {self.rating}>"
    
    @classmethod
    def find_by_product(cls, product_id):
        """Fetch reviews for a specific product."""
        return cls.query.filter_by(product_id=product_id).all()

    @classmethod
    def find_by_service(cls, service_id):
        """Fetch reviews for a specific service."""
        return cls.query.filter_by(service_id=service_id).all()
