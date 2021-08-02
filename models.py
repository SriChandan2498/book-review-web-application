from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):  
    _tablename_ = 'register'
    name = db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False, primary_key=True)
    pswd = db.Column(db.String,nullable=False)
    timestamp = db.Column(db.DateTime,nullable=False)