"""
A module for shipping model
"""
from . import db
from .baseModel import BaseModel
import enum


# Enums for Order Status and Payment Status
class ShippingStatus(enum.Enum):
    """class showing different order statuses"""
    PENDING = 'pending'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'


class Shipping(BaseModel):
    """ Model that handles shipping of orders"""
    __tablename__ = 'shipping'
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shipping_address = db.Column(db.String(255), nullable=False)
    shipping_method = db.Column(db.String(50), nullable=False)

    # Using Enums for status
    status = db.Column(
        db.Enum(ShippingStatus),
        nullable=False,
        default=ShippingStatus.PENDING
        )
    shipping_status = db.Column(
        db.String(50),
        nullable=False,
        default='pending'
        )
    shipped_date = db.Column(db.DateTime, nullable=True)
    delivery_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='shipping')
    order = db.relationship('Order', back_populates='shipping')

    def __repr__(self):
        return f"<Shipping {self.id} - Order: {self.order_id}, Status: {self.shipping_status}>"
