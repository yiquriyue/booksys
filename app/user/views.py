#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera, get_userinfo
from werkzeug import secure_filename
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
from flask_login import login_user,logout_user
from app.send_email import send_email
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
            session['route'] = 'user'
            session.permanent = True
            user = get_userinfo(check)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('user_login.html')
    if request.method == 'GET':
        return render_template('user_login.html')

@app.route('/user/logout')
def logout():
    logout_user()
    if 'route' in session:
        session.pop('route')
    return redirect(url_for('home'))

@app.route('/user/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        phone = request.form['sms']
        manager = DBOpera()
        check = manager.user_register(username,password,email,phone)
        if check:
            return redirect(url_for('.login'))
        else:
            return render_template('user_register.html')
    if request.method == 'GET':
        return render_template('user_register.html')
        
@app.route('/user/confirm/<token>',methods=['GET','POST'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('home'))
    if current_user.confirm(token):
        flash('success！','ok')
    else:
        flash('faild！pless try again！','fail')
    return redirect(url_for('home'))

@app.route('/user/reconfirm')
def re_confirm():
    token = current_user.get_confirmation()
    send_email(current_user.user_email,'Confirm Your Account','user/confirm_1',user=current_user,token=token)
    flash("plese check in your email!",'again')
    return redirect(url_for('home'))
    
# @app.before_request
# def before_request():
    # if (current_user.is_authenticated and not current_user.confirmed \
        # and request.endpoint[:5]!='auth.' and request.endpoint !='static'):
        # return redirect(url_for('unconfirmed'))

@app.route('/user/unconfirmed')        
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home'))
    return render_template('unconfirmed.html')
    
@app.route('/user/homepage',methods=['GET','POST'])
@login_required
def homepage():
    if current_user.is_authenticated:
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

@app.route('/user/cart',methods=['GET','POST'])
def cart():
    if request.method =='GET':
        manager = DBOpera()
        carts = manager.get_cart(current_user.id)
        
        return render_template('user_shopping_cart.html',carts = carts)

@app.route('/user/collect',methods=['GET','POST'])
def collect():
    if request.method =='GET':
        manager = DBOpera()
        books = manager.get_collect(current_user.id)
        book_list = []
        a=1
        for book in books:
            abook={}
            abook['no'] = a
            abook['id'] = str(book.book_id)
            abook['name'] = book.book_name
            abook['author'] = book.book_author
            abook['message'] = book.book_message
            abook['price'] = book.book_price
            abook['num'] = book.book_num
            if book.book_image:
                abook['image'] = 'files/'+abook['id']+'/'+book.book_image
            else:
                abook['image'] = ''
            book_list.append(abook)
        return render_template('user_collect.html',collects = book_list)