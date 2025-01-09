from . import db
from .baseModel import BaseModel

class Service(BaseModel):
    """ A service model that inherites from BaseModel"""
    __tablename__ = 'services'
    name = db.Column(
        db.String(100),
        nullable = False
        )
    business_id = db.Column(
        db.Integer,
        db.ForeignKey(
             'business.id',
            name='fk_service_business'
             ),
        nullable = False
        )
    wishlist_id = db.Column(
        db.Integer,
        db.ForeignKey('wishlist.id', name='fk_service_wishlist'),
        nullable = True
        )
    
    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id', name='fk_service_category'),
        nullable = False
    )

    payment_id = db.Column(
        db.Integer,
        db.ForeignKey('payments.id', name='fk_service_payment'),
        nullable = False
    )
    
    order_id = db.Column(
        db.Integer,
        db.ForeignKey(
             'orders.id',
            name='fk_service_order'
             ),
        nullable = False
        )
    description = db.Column(
        db.Text,
        nullable = False
        )
    hourly_cost = db.Column(
        db.Float,
        nullable = False
        )
    duration = db.Column(
        db.Integer,
        nullable = False
    )

    # Relationship to access related business easily
    inventory = db.relationship('Inventory', back_populates='service')
    business = db.relationship('Business', back_populates='services')
    reviews =db.relationship('Review', back_populates='service')
    category = db.relationship('Category', back_populates='service')
    orders = db.relationship(
         'Order',
         back_populates='service',
        foreign_keys='Order.service_id'
         )
    payment = db.relationship(
         'Payment',
         back_populates='service',
        foreign_keys='Payment.service_id'
         )
    wishlist = db.relationship(
         'Wishlist',
         back_populates='service',
        foreign_keys='Wishlist.service_id'
         )

    def __repr__(self):
         return f"<Service {self.name}, Hourly Cost: {self.hourly_cost}>"
    
    