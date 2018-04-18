#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 

@app.route('/book/list',methods=['GET','POST'])
def book_list():
    if request.method == 'GET':
        db = DBOpera()
        #TODO(caoyue):在图书表中查找图书
        
@app.route('/book/select',methods=['POST'])
def book_select():
    if request.method == 'POST':
        bookname = request.form['bookname']
        bookathor = request.form['bookathor']
        