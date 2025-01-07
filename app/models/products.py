from . import db
from .baseModel import BaseModel


class Product(BaseModel):
    """ A product model class that inherites from BaseModel"""
    __tablename__ = 'products'
    name = db.Column(
        db.String(100),
        nullable = False
        )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey('business.id'),
        nullable = False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable = False
    )

    payment_id = db.Column(
        db.Integer,
        db.ForeignKey('payment.id'),
        nullable = False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id'),
        nullable = False
    )

    payment_d = db.Column(
        db.Integer,
        db.ForeignKey('payments.id'),
        nullable = False
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id'),
        nullable = True
        )

    wishlist_id = db.Column(
        db.Integer,
        db.ForeignKey('wishlist.id'),
        nullable = True
        )

    description = db.Column(
        db.Text,
        nullable = False
        )
    price = db.Column(
        db.Float,
        nullable = False
        )
    quantity = db.Column(
        db.Integer,
        nullable = False
    )
    stock = db.Column(
        db.Integer,
        default = 0
    )

    # Relationships
    category = db.relationship('Category', back_populates='product')
    reviews = db.relationship('Review', back_populates='product')
    business = db.relationship('Business', back_populates='product')
    payment = db.relationship('Payment', back_populates='product')
    order = db.relationship('Order', back_populates='product')
    wishlist = db.relationship('Wishlist', back_populates='product')
