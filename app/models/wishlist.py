from . import db
from .baseModel import BaseModel

class Wishlist(BaseModel):
    __tablename__ = 'wishlist'
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    
    user = db.relationship('User', back_populates='wishlist')
    product = db.relationship('Product', back_populates='wishlist')
    service = db.relationship('Service', back_populates='wishlist')

    def __repr__(self):
        return f"<Wishlist {self.id} - User: {self.user_id}, Product: {self.product_id}>"
