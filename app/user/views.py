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
    '''
    用户登陆
    '''
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
    '''
    用户登出
    '''
    logout_user()
    if 'route' in session:
        session.pop('route')
    return redirect(url_for('home'))

@app.route('/user/register',methods=['GET','POST'])
def register():
    '''
    用户注册
    '''
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
    '''
    用户激活验证
    '''
    if current_user.confirmed:
        return redirect(url_for('home'))
    if current_user.confirm(token):
        flash('success！','ok')
    else:
        flash('faild！pless try again！','fail')
    return redirect(url_for('home'))

@app.route('/user/reconfirm')
def re_confirm():
    '''
    用户再次发送激活邮件
    '''
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
    '''
    用户未激活
    '''
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home'))
    return render_template('unconfirmed.html')
    

@app.route('/user/password',methods=['GET','POST'])
def password():
    return render_template('user_Password.html')

@app.route('/user/cart',methods=['GET','POST'])
def cart():
    '''
    用户购物车
    '''
    if request.method =='GET':
        manager = DBOpera()
        carts = manager.get_cart(current_user.id)
        list = []
        list1 = []
        for cart in carts:
            dict = {}
            dict1={}
            dict["book_id"]= int(cart[0].book_id)
            dict1["book_id"]= int(cart[0].book_id)
            dict["book_name"]= cart[0].book_name
            dict["book_price"]= cart[0].book_price
            if cart[0].book_image:
                dict["book_image"] = 'files/'+str(dict["book_id"])+'/'+cart[0].book_image
            else:
                dict["book_image"] = ''
            dict["book_num"]= int(cart[1])
            dict1["book_num"]= int(cart[1])
            list.append(dict)
            list1.append(dict1)
        return render_template('user_shopping_cart.html',books = list,book_id=list1)


        
        
@app.route('/user/collect',methods=['GET','POST'])
def collect():
    '''
    用户收藏夹
    '''
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
        
@app.route('/user/home',methods=['GET','POST'])
@login_required
def user_home():
    '''
    用户信息展示
    '''
    if request.method == 'GET':
        return render_template('user_contact_us.html',userName= current_user.user_name,
            iphone= current_user.user_phone,email= current_user.user_email)
    if request.method == 'POST':
        password=request.form['password']
        new_password=request.form['new_password']
        email=request.form['email']
        phone=request.form['phone']
        manager = DBOpera()
        check = manager.user_check(current_user.user_name,password)
        if check:
            manager.update_user(new_password,email,phone)
            return redirect(url_for('user_home'))
        else:
            return "密码错误"
        

@app.route('/user/order',methods=['GET','POST'])
def user_order():
    db = DBOpera()
    if request.method == 'GET':
        order_lists = db.get_orderList(current_user.user_name)
        return render_template('user_order_list.html',order_lists = order_lists)
        
@app.route('/user/order/<order_id>',methods=['GET','POST'])
def order_detail(order_id):
    db = DBOpera()
    if request.method == 'GET':
        books = db.get_orderAttach(order_id)
        list = []
        for cart in books:
            dict = {}
            dict["book_id"]= int(cart[0].book_id)
            dict["book_name"]= cart[0].book_name
            dict["book_price"]= cart[0].book_price
            if cart[0].book_image:
                dict["book_image"] = 'files/'+str(dict["book_id"])+'/'+cart[0].book_image
            else:
                dict["book_image"] = ''
            dict["book_num"]= int(cart[1])
            list.append(dict)
        price = db.get_orderPrice(order_id)
        return render_template('user_orderAttach.html',book_list=list,price=price,order_id=order_id)
        
    
@app.route('/user/shelf',methods=['GET','POST'])
def bookshelf():
    if request.method == 'GET':
        route = session.get('route')
        #search = request.form['search']
        db = DBOpera()
        books = db.get_userBoughtBook(current_user.id)
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
            a=a+1
        return render_template('user_shelf.html',book_list=book_list)