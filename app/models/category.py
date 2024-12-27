from . import db
from .baseModel import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'
    
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    products = db.relationship('Product', back_populates='category')
    order = db.relationship('Order', back_populates='category')

    def __repr__(self):
        return f"<Category {self.id} - Name: {self.name}>"
