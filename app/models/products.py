"""
A module for a product model
"""
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
        db.ForeignKey('business.id', 
                    name='fk_product_business'
                      ),
        nullable = False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', 
                    name='fk_product_category'
                      ),
        nullable = False
    )

    payment_id = db.Column(
        db.Integer,
        db.ForeignKey('payments.id', 
                    name='fk_product_payment'
                      ),
        nullable = False
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id', 
                    name='fk_product_order'
                      ),
        nullable = True
        )

    wishlist_id = db.Column(
        db.Integer,
        db.ForeignKey('wishlist.id',
                    name='fk_product_wishlist'
                    ),
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
    inventory = db.relationship('Inventory', back_populates='product')
    category = db.relationship('Category', back_populates='product')
    reviews = db.relationship('Review', back_populates='product')
    business = db.relationship('Business', back_populates='product')
    payment = db.relationship(
        'Payment',
        back_populates='product',
        foreign_keys='Payment.product_id'
        )
    orders = db.relationship(
        'Order',
        back_populates='product',
        foreign_keys='Order.product_id'
        )
    wishlist = db.relationship(
        'Wishlist',
        back_populates='product',
        foreign_keys='Wishlist.product_id'
        )
