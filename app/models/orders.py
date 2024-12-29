from . import db
from .baseModel import BaseModel
from datetime import datetime, timezone
import enum


# Enums for Order Status and Payment Status
class OrderStatus(enum.Enum):
    """class showing different order statuses"""
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'


class PaymentStatus(enum.Enum):
    """ class showing different payment statuses"""
    PAID = 'paid'
    UNPAID = 'unpaid'
    REFUNDED = 'refunded'


class Order(BaseModel):
    """Model representing customer orders."""
    
    __tablename__ = 'orders'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    total_price = db.Column(db.Float, nullable=False)
    
    # Using Enums for status and payment_status
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    payment_status = db.Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.UNPAID)
    
    payment_method = db.Column(db.String(255), nullable=True)  # e.g., credit card, PayPal
    shipping_address = db.Column(db.String(255), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    delivery_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='orders')
    service = db.relationship('Service', back_populates='orders')
    product = db.relationship('Product', back_populates='orders')
    payment = db.relationship('Payment', back_populates='order')
    category = db.relationship('Category', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id} - User: {self.user_id}, Status: {self.status.value}>"
