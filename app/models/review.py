from . import db
from datetime import datetime, timezone
from .baseModel import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # e.g., 1-5
    comment = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    user = db.relationship('User', back_populates='reviews')
    product = db.relationship('Product', back_populates='reviews')
    service = db.relationship('Service', back_populates='reviews')
    business = db.relationship('Business', back_populates='reviews')


    def __repr__(self):
        return f"<Review {self.id} - Product: {self.product_id}, Rating: {self.rating}>"
