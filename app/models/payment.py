from . import db
from datetime import datetime, timezone
from .baseModel import BaseModel

class Payment(BaseModel):
    """ Handles payments for orders, products, services etc"""
    __tablename__ = 'payments'
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    payment_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., credit card, PayPal
    payment_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='unpaid')  # e.g., paid, refunded
    
    order = db.relationship('Order', back_populates='payment')
    service = db.relationship('Service', back_populates='payment')
    product= db.relationship('Product', back_populates='payment')

    def __repr__(self):
        return f"<Payment {self.id} - Order: {self.order_id}, Status: {self.payment_status}>"
