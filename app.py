from flask import Flask,render_template,request,session
from operator import and_
from models import *
import os
from werkzeug.utils import redirect
import datetime

app = Flask(__name__) # creates new web application and '__name__' = current file name
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "any random string"

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/") # Decorator : part of url of the web page
def index():
    flag = False
    if 'email' in session:
        email = session['email']
        flag = True
        return render_template("user.html",user=email)
    return render_template('index.html')

@app.route('/signup', methods = ['POST','GET'])
def signup():
    return render_template('register.html')

@app.route('/signupaction', methods = ['POST'])
def signupAction():
    render_template('register.html')
    name = request.form.get('name')
    email = request.form.get('email')
    pswd = request.form.get('pswd')
    record = Users(name = name,email=email,pswd=pswd,timestamp=datetime.datetime.now())
    db.session.add(record)
    db.session.commit()
    return f'<h1 style = "padding-top: 20%; text-align:center">{name.capitalize()}, Thank you for Registering.</h1>'
        

@app.route('/login',methods = ['POST',"GET"])
def login():
    method = request.method
    if(method == 'GET'):
        return render_template("index.html")
    else:
        email = request.form.get('email')
        pswd = request.form.get('pswd')

        try:
            user = Users.query.filter(and_(Users.email==email,Users.pswd == pswd))
            if user.email != None:
                session['email'] = email
            return render_template("index.html",flag=True)               
        except:
            session['email'] = email
            return render_template("user.html",user=email)

@app.route('/admin',methods=['GET'])
def admin():
    details = Users.query.all()
    return render_template('admin.html', details=details)

@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop('email',None)
    return redirect('/')