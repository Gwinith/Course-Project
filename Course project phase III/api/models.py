from flask_sqlalchemy import SQLAlchemy
from api import db

class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(100), primary_key=True)
    fname = db.Column(db.String(50), nullable=False) 
    lname = db.Column(db.String(50), nullable=False) 
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False) 
    category_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer)


class Dashboard(db.Model):
    __tablename__ = 'dashboard'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    email= db.Column(db.String(100))
    product_name = db.Column(db.String(50), nullable=False) 
    category_name = db.Column(db.String(50), nullable=False)
    status= db.Column(db.String(50), nullable=False)

db.create_all()