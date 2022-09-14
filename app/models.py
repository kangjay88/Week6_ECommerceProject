from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

db = SQLAlchemy()  #this will translate SQL into Python

cart = db.Table('cart',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

#create our Models based off of our ERD
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique = True)
    email = db.Column(db.String(150), nullable=False, unique = True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)
    cart = db.relationship("Product",
        secondary = cart,
        backref = 'shoppers',
        lazy = 'dynamic'
        )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def add(self, product):
        self.cart.append(product)
        db.session.commit()

    def delete(self, product):
        self.cart.remove(product)
        db.session.commit()
    
    def myCart(self):
        mycart = Product.query.join(cart, (Product.id == cart.c.product_id)).filter(cart.c.user_id == self.id)
        return mycart 

    def deleteall(self):
        db.session.query(cart).delete()
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'token': self.apitoken
        }
        
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String(300))
    description = db.Column(db.String(300))
    price = db.Column(db.Numeric(10,2))

    def __init__(self, name,img,desc,price):
        self.product_name = name
        self.img_url = img
        self.description = desc
        self.price = price

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'img_url': self.img_url,
            'description': self.description,
            'price': self.price
        }