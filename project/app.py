from flask import Flask,render_template, request, session
# from flask.wrappers import Request
from operator import and_
from models import *
import os
from werkzeug.utils import redirect
import pandas as pd

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = "any random string"
with app.app_context():
    db.create_all()

@app.route("/home")
def demo():
    flag = False
    if 'email' in session:
        email = session['email']
        flag = True
        return render_template("mainpage.html",user=email,flag=True)
    return render_template("mainpage.html",flag = False)

@app.route("/forms", methods=["POST","GET"])
def forms():
    if(request.method=="GET"):
        return render_template("index.html")
    else:
        fname=request.form.get("fname")
        lname=request.form.get("lname")
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        try:
            alreadyanuser = Users.query.filter(Users.email==email).first()
            if alreadyanuser.email != None:
                session['email'] = email
                return render_template("index.html",flag=True)               
        except:
            details=Users(firstname=fname,lastname=lname,email=email,pwd=pwd)
            session['email'] = email
            db.session.add(details)
            db.session.commit()
            return redirect('/home')

@app.route("/login", methods=["POST","GET"])
def login():
    if(request.method=="GET"):
        return render_template("loginpage.html")
    else:
        try:
            email=request.form.get("email")
            pwd=request.form.get("pwd")
            user=Users.query.filter(and_(Users.email==email, Users.pwd==pwd)).first()
            session['email'] = user.email
            return redirect('/home')
        except:
            return render_template("loginpage.html",flag=True)

@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop('email',None)
    return redirect('/home')

@app.route("/books",methods=["POST","GET"])
def books():
    if request.method == "POST":
        val=request.form.get("books")
        searchname=request.form.get("searchname")
        tag = '%'+searchname+'%'
        if(val=="all"):
            book1 = Bookdetails.query.filter(Bookdetails.id.ilike(tag)).all()
            book2 = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
            book3 = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
            book4 = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
            book = book1+book2+book3+book4
        elif(val=="id"):
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.id.ilike(tag)).all()
        elif(val=="title"):
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
        elif(val=="author"):
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
        elif(val=="year"):
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
            # book=Bookdetails.query.filter_by(val)
        print(book)
        email = session['email']
        flag = True
        return render_template("mainpage.html",email = email,flag = flag,books=book)
    else:
        return redirect('/home')

@app.route("/id/<id>",methods=["POST","GET"])
def id(id):
    return f"isbn number {id}"