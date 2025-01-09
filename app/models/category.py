from . import db
from models.baseModel import BaseModel

class Category(BaseModel):
    __tablename__ = 'categories'
    
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    
    product = db.relationship('Product', back_populates='category')
    service = db.relationship('Service', back_populates='category')
    orders = db.relationship('Order', back_populates='category')

    def __repr__(self):
        return f"<Category {self.id} - Name: {self.name}>"
    

    @classmethod
    def name_exists(cls, name: str):
        """Check if a name already exists in the database"""
        return cls.query.filter_by(name=name).first() is not None

    @classmethod
    def description_exists(cls, description: str):
        """Check if an email already exists in the database"""
        return cls.query.filter_by(description=description).first() is not None

    def save(self):
        """Save current object to the database with validation"""
        if Category.name_exists(self.name):
            raise ValueError("Name already taken.")
        
        if Category.description_exists(self.description):
            raise ValueError("Description already in use.")
        db.session.add(self)
        db.session.commit()
