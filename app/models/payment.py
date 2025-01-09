from . import db
from datetime import datetime, timezone
from .baseModel import BaseModel

class Payment(BaseModel):
    """ Handles payments for orders, products, services etc"""
    __tablename__ = 'payments'
    
    order_id = db.Column(db.Integer, db.ForeignKey(
        'orders.id',
        name='fk_payment_order'
        ),
        nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id',
        name='fk_payment_service'
        ),
        nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id',
        name='fk_payment_product'
        ), nullable=True)
    payment_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    payment_method = db.Column(db.String(50), nullable=False)  # e.g., credit card, PayPal
    payment_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='unpaid')  # e.g., paid, refunded
    
    orders = db.relationship(
        'Order',
        back_populates='payment',
        foreign_keys='Payment.order_id'
        )
    service = db.relationship(
        'Service',
        back_populates='payment',
        foreign_keys='Payment.service_id'
        )
    product= db.relationship(
        'Product',
        back_populates='payment',
        foreign_keys='Payment.product_id'
        )

    def __repr__(self):
        return f"<Payment {self.id} - Order: {self.order_id}, Status: {self.payment_status}>"
