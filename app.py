from flask import Flask,render_template, request, session, jsonify
# from flask.wrappers import Request
from operator import and_
import datetime
from models import *
import os
from werkzeug.utils import redirect
import pandas as pd
from flask.helpers import flash, url_for

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('HEROKU_DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = "any random string"
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("user.html")

@app.route("/forms", methods=["POST","GET"])
def forms():
    if(request.method=="GET"):
        return render_template("loginpage.html")
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
            
            details=Users(firstname=fname,lastname=lname,email=email,pwd=pwd,timestamp=datetime.datetime.now())
            session['email'] = email
            db.session.add(details)
            db.session.commit()
            return redirect('/')

@app.route("/login", methods=["POST","GET"])
def login():
    if(request.method=="GET"):
        return render_template("index.html")
    else:
        try:
            email=request.form.get("email")
            pwd=request.form.get("pwd")
            user=Users.query.filter(and_(Users.email==email, Users.pwd==pwd)).first()
            session['email'] = user.email
            return redirect('/')
        except:
            return render_template("index.html",flag=True)

@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop('email',None)
    return redirect('/')

@app.route("/api/search",methods=["POST","GET"])
def books():
    if request.method == "POST":
        val=request.form.get("books")
        searchname=request.form.get("searchname")
        tag = '%'+searchname+'%'
        if(val=="isbn"):
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.isbn.ilike(tag)).all()
        elif(val=="title"):
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
        elif(val=="author"):
           
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
        elif(val=="year"):
           
            print("val=",val)
            book = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
        data = list()
        for each in book:
            data.append({"isbn":each.isbn,"title":each.title,"author":each.author,'year':each.year})
        return jsonify(data)
    else:
        return redirect('/')

@app.route("/api/book_details/<bookdetail>",methods = ["GET"])
def getDetails(bookdetail):
    book = ''
    if(bookdetail.isdigit()):
        book = Bookdetails.query.filter(Bookdetails.isbn == bookdetail).first()
    else:
        book = Bookdetails.query.filter(Bookdetails.title == bookdetail).first()
    return jsonify({"isbn":book.isbn,"title":book.title,"author":book.author,'year':book.year})

@app.route("/id/<id>",methods=["POST","GET"])
def id(id):
    det = Bookdetails.query.filter(Bookdetails.isbn==id).all()
    reviews_display = reviews.query.filter(reviews.id==id).all()
    session['id'] = id
    email=session['email']
    flag_review = False
    delbook=False
                # flash("Book is added into Shelf")
    if 'email' in session:
        email = session['email']
        try:
            s = shelf.query.filter(and_(shelf.id==id, shelf.email==email)).first()
            print("shelf submit files = ",s.email,s.isbn)
            delbook=True
        except:
            delbook=False
        try:
            existing_user = reviews.query.filter(and_(reviews.id==id,reviews.email==email)).first()
            if existing_user.email != None:
                flag_review = False
        except:
           
            flag_review = True
    
        return render_template('review.html',delbook=delbook,reviews=reviews_display,uname=email,flag_review=flag_review,flag=True,details=det)
    else:
        return render_template('review.html',reviews=reviews_display,flag_review=flag_review,flag=False,details=det)

@app.route("/review", methods=['POST','GET'])
def review():
    if request.method == 'GET':
        return render_template('review.html')
    else:
        review = request.form.get('review')
        rating = request.form.get('rating')
        email = session['email']
        id = session['id']
        # print("from /review , user= ",user," book = ",bookid)
        add_review = reviews(id=id,email=email,review=review,rating=int(rating))
        db.session.add(add_review)
        db.session.commit()
        det = Bookdetails.query.filter(Bookdetails.isbn==id).all()
        reviews_display = reviews.query.filter(reviews.id==id).all()
        return render_template('review.html', reviews=reviews_display, flag_review=False, uname=email, flag=True, details=det)

@app.route('/addtoshelf', methods=['POST','GET'])
def addtoshelf():
    if request.method == 'GET':
        return redirect('/')
    else:
        id = session['id']
        det = Bookdetails.query.filter(Bookdetails.isbn==id).all()
        total_reviews = reviews.query.filter(reviews.id==id).all()
        flag_review = False
        delbook=False
        if 'email' in session:
            
            # count = request.form.get('shelf')
            email = session['email']
            try:
                s = shelf.query.filter(and_(shelf.id==id, shelf.email==email)).delete()
                db.session.commit()
                if s == 0:
                    print("shelf submit files = ",s.email,s.id)
                delbook=False
                flash("Book is deleted from Shelf")
            except:
                tit=Bookdetails.query.filter(Bookdetails.isbn==id).first()
                print(tit.isbn)
                s = shelf(id=id,title=tit.title,email=email)
                db.session.add(s)
                db.session.commit()
                delbook=True
                flash("Book is added into Shelf")
            try:
                rev = reviews.query.filter(and_(reviews.id==id,reviews.email==email)).first()
                if rev.email != None:
                    flag_review = False
            except Exception as e:
                print("exception while clicked on id = ",e)
                flag_review = True 
            return render_template('review.html',delbook=delbook,reviews=total_reviews,uname=email,flag_review=flag_review,flag=True,details=det)
        else:
           return render_template('review.html',delbook=delbook,reviews=total_reviews,flag_review=flag_review,flag=False,details=det)
           

@app.route("/openshelf",methods=['POST','GET'])
def openshelf():
    if 'email' in session:
        email = session['email']
        try:
            books = shelf.query.filter(shelf.email==email).all()
            # det = Bookdetails.query.filter(Bookdetails.isbn==boo).all()
            return render_template("shelf_display.html",books=books,flag=True,uname=email)
        except:
            return render_template('shelf_display.html',msg=True,flag=True,uname=email)
    else:
        pass

@app.route("/home",methods=["POST","GET"])
def home():
    return redirect('/')

@app.route('/admin',methods=['GET'])
def admin():
    details = Users.query.all()
    return render_template('admin.html', details=details)


