#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
from flask import request
from flask import render_template
from flask import flash
from flask import abort
from flask import url_for
from flask import redirect
from flask import session
from flask import Flask
from app import app
#from app.models import DBOpera 

@app.route('/home',methods=['GET','POST'])
def home():
    '''
    用户主页
    '''
    if request.method == 'GET':
        return render_template('login.html')