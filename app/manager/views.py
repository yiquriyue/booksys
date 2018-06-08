#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera ,get_userinfo


@app.route('/manager/login',methods=['GET','POST'])
def manager_login():
    '''
    管理员登陆验证
    '''
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        manager = DBOpera()
        check = manager.manager_check(username,password)
        if check:
            session['username'] = username
            session['userid'] = check
            session['route'] = 'manager'
            session.permanent = True
            user = get_userinfo(check)
            login_user(user)
            return redirect(url_for('book_list'))
        else:
            return render_template('manage_login.html')
    if request.method == 'GET':
        return render_template('manage_login.html')

        
