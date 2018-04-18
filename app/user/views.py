#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 
from werkzeug import secure_filename
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route('/user/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        manager = DBOpera()
        check = manager.user_check(username,password)
        if check:
            session['username'] = username
            session['userid'] = check
            session.permanent = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/user/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        phone = request.form['sms']
        manager = DBOpera()
        check = manager.user_register(username,password,email,phone)
        print check
        if check:
            return redirect(url_for('.login'))
        else:
            return render_template('register.html')
    if request.method == 'GET':
        return render_template('register.html')

@app.route('/user/homepage',methods=['GET','POST'])
def homepage():
	userid = session.get('userid')
	if userid:
	    if request.method == 'GET':
	    	manager = DBOpera()
	    	user = manager.get_userinfo(userid)
	        return render_template('userData.html',userName= user.user_name,
	        	password= user.user_password,iphone= user.user_phone,email= user.user_email)
	else:
		 return render_template('login.html')      

@app.route('/user/password',methods=['GET','POST'])
def password():
    return render_template('user_Password.html')
