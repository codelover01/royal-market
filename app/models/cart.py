from . import db
from models.baseModel import BaseModel

class Cart(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='cart', lazy=True)
    products = db.relationship('Product', secondary='cart_product', lazy='subquery', backref=db.backref('carts', lazy=True))

class CartProduct(BaseModel):
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
