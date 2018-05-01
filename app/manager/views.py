#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 


@app.route('/manager/login',methods=['GET','POST'])
def manager_login():
    '''
    管理员登陆验证
    '''
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        manager = DBOpera()
        check = manager.user_check(username,password)
        if check:
            session['username'] = username
            session['userid'] = check
            session['route'] = 'manager'
            session.permanent = True
            return redirect(url_for('home'))
        else:
            return render_template('manage_login.html')
    if request.method == 'GET':
        return render_template('manage_login.html')

@app.route('/manager/register',methods=['GET','POST'])
def manager_register():
    '''
    管理员注册
    '''
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

@app.route('/manager/homepage',methods=['GET','POST'])
def manager_homepage():
    '''
    管理员首页
    '''
    userid = session.get('userid')
    if userid:
        if request.method == 'GET':
            manager = DBOpera()
            user = manager.get_userinfo(userid)
            return render_template('userData.html',userName= user.user_name,
                password= user.user_password,iphone= user.user_phone,email= user.user_email)
    else:
         return render_template('login.html')      

@app.route('/manager/password',methods=['GET','POST'])
def manager_password():
    return render_template('user_Password.html')
