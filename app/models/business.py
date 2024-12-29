from . import db
from .baseModel import BaseModel


class Business(BaseModel):
    """A business model class that inherites from BaseModel"""
    name = db.Column(
        db.String(255),
        nullable = False,
        unique = True
        )
    email = db.Column(
        db.String(255),
        nullable = False,
        unique = True
        )
    description = db.Column(
        db.Text,
        nullable = False
    )
    location = db.Column(
        db.String(255),
        nullable = False
    )
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    online_available = db.Column(
        db.Boolean,
        default=True
        )
    offline_available = db.Column(
        db.Boolean,
        default=True
        )
    
    # Relationships
    user = db.relationship('User', back_populates='business')
    product = db.relationship('Product', back_populates='business')
    service = db.relationship('Service', back_populates='business')
    reviews = db.relationship('Reviews', back_populates='business')