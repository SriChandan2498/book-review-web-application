from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    _tablename_ = 'register'
    firstname = db.Column(db.String,nullable=False)
    lastname = db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False, primary_key=True)
    pwd = db.Column(db.String,nullable=False)

class Bookdetails(db.Model):
    __tablename__= 'Bookdetails'
    id = db.Column(db.String,primary_key=True)
    title = db.Column(db.String,nullable=False)
    author = db.Column(db.String,nullable=False)
    year = db.Column(db.String,nullable=False)

class reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.String,primary_key=True)
    email = db.Column(db.String,primary_key=True)
    review = db.Column(db.String,nullable=False)
    rating = db.Column(db.Integer,nullable=False)

class shelf(db.Model):
    __tablename__='shelf'
    id = db.Column(db.String,primary_key=True)
    title=db.Column(db.String,nullable=False)
    email = db.Column(db.String,primary_key=True)

    