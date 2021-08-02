from flask import Flask,render_template,request
from models import *
import datetime
import os

app = Flask(__name__) # creates new web application and '__name__' = current file name
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "any random string"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/") # Decorator : part of url of the web page
def index():
    return render_template('index.html')

@app.route('/login',methods = ['POST'])
def login():
    method = request.method
    if(method == 'GET'):
        return f'<h1 style = "padding-top: 20%; text-align:center">You are logged-in</h1>'
    else:
        name = request.form.get('name')
        email = request.form.get('email')
        pswd = request.form.get('pswd')
        record = Users(name = name,email=email,pswd=pswd,timestamp=datetime.datetime.now())
        db.session.add(record)
        db.session.commit()
        return f'<h1 style = "padding-top: 20%; text-align:center">{name.capitalize()}, Thank you for Registering.</h1>'
        
@app.route('/admin',methods=['GET'])
def admin():
    details = Users.query.all()
    return render_template('admin.html', details=details)