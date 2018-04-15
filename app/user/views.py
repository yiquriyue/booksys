#encoding:utf-8
from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
from app import db
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 


@app.route('/user/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['telphone']
        password=request.form['password']
        manager = DBOpera()
        print username
        print password
        check = manager.user_check(username,password)
        if check:
            return render_template('index.html')
        else:
            return render_template('login.html')
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/user/password',methods=['GET','POST'])
def password():
    return render_template('user_Password.html')

'''
@app.route('/',methods=['GET','POST'])
def submit():
    error = None
    date=None
    foodlist=food.query.filter_by(fclass='food').all()
    drinklist=food.query.filter_by(fclass='drink').all()
    if request.method == 'POST':
    #render_template('register.html',error = error)
        userfood = request.form['userfood']
        drink = request.form['drink']
        name = request.form['name']
        date =request.form['date']
        if list.query.filter_by(name=name,date=date).count():
            user=list.query.filter_by(name=name,date=date).first()
            user.drink=drink
            user.food=userfood
        else:
            information = list(name,userfood,drink,date)
            db.session.add(information)
        db.session.commit()
        flash('order success')
    return render_template('index.html', error=error,date=date,foodlist=foodlist,drinklist=drinklist)

@app.route('/user/<date>')
def show_user(date):
    users=list.query.filter_by(date=date).all()
    #user = list.query.filter_by(date=date).first_or_404()
    print users
    return render_template('list.html', users=users)

@app.route('/addfood',methods=['GET','POST'])
def addfood():
    if request.method == 'POST':
        fclass = request.form['fclass']
        print fclass
        name = request.form['name']
        if food.query.filter_by(name=name).count():
            flash('add faliure')
        else:
            information = food(name,fclass)
            db.session.add(information)
            db.session.commit()
            flash('add success')
    return render_template('addfood.html')
'''
