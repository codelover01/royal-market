"""
A module for Inventory model
"""
from . import db
from datetime import datetime, timezone
from .baseModel import BaseModel

class Inventory(BaseModel):
    """ A model for the business inventory """
    __tablename__ = 'inventory'
    
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id',
        name='fk_invenory_product'
        ),
        nullable = False)
    service_id = db.Column(db.Integer, db.ForeignKey(
        'services.id',
         name='fk_invenory_service'
        ),
        nullable = False)
    stock = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
        )
    
    product = db.relationship('Product', back_populates='inventory')
    service = db.relationship('Service', back_populates='inventory')

    def __repr__(self):
        """ Returns a string representation of an inventory object """
        return f"<Inventory {self.id} - Product: {self.product_id}, Stock: {self.stock}>"
