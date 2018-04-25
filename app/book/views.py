#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 
from flask_login import login_required
from werkzeug import secure_filename
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
from app.setting import UPLOAD_FOLDER
import shutil
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/book/list',methods=['GET','POST'])
@login_required
def book_list():
    if request.method == 'GET':
        route = session.get('route')
        #search = request.form['search']
        db = DBOpera()
        books = db.get_bookList()
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
        if route=='user':
            return render_template('user_catalog_list.html',book_list=book_list)
        else:
            return render_template('manage_booklist.html',book_list=book_list)
        
        #TODO(caoyue):在图书表中查找图书
                               
@app.route('/book/add',methods=['GET','POST'])
def book_add():
    db = DBOpera()
    if request.method == 'GET':
        class_list = db.get_classList()
        return render_template('manage_newbook.html',class_list=class_list)
    if request.method =='POST':
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        book_price = request.form['book_price']
        book_class = request.form['book_class']
        book_message = request.form['book_message']
        file = request.files['book_image']
        book_num = request.form['book_num']
        book_id = db.add_book(book_name,book_author,book_class,book_price,book_num,book_message)
        if file and allowed_file(file.filename):
            if os.path.exists(os.path.join(UPLOAD_FOLDER,str(book_id))):
                shutil.rmtree(os.path.join(UPLOAD_FOLDER,str(book_id)))
            os.mkdir(os.path.join(UPLOAD_FOLDER,str(book_id)))
            filename = 'buddha.' + file.filename.rsplit('.', 1)[1]
            book_image = os.path.join(UPLOAD_FOLDER,str(book_id),filename)
            fp = open(book_image,'w')
            file.save(book_image)
            fp.close()
            db.add_bookImag(book_id,filename)
        return redirect(url_for('book_add'))

@app.route('/book/detail/<book_id>',methods=['POST','GET','PUT'])
def book_detail(book_id):
    if request.method == 'GET':
        db = DBOpera()
        book = db.get_bookAttach(book_id)
        abook={}
        abook['id'] = str(book.book_id)
        abook['name'] = book.book_name
        abook['author'] = book.book_author
        abook['message'] = book.book_message
        abook['price'] = book.book_price
        if book.book_image:
                abook['image'] = 'files/'+abook['id']+'/'+book.book_image
        else:
            abook['image'] = ''
        return render_template('user_product_page.html',book=abook)

        
@app.route('/book/collect',methods=['GET','POST'])
def book_collect():
    if request.method == 'POST':
        user_id = session.get('userid')
        book_id = request.form['book_id']
        db = DBOpera()
        db.add_collect(book_id,user_id)
        return "success"
        
        
@app.route('/book/cart',methods=['GET','POST'])
def book_cart():
    if request.method == 'POST':
        book_id = request.form['book_id']
        db = DBOpera()
        db.add_cart(book_id,current_user.id)
        return "success"
        
@app.route('/book/add_detail',methods=['GET','POST']
def add_detail():
    if request.method=='POST':
        carts = session.get('carts')
        #数据库操作生成订单，返回订单编号
        db = DBOpera()
        orders = db.add_order(current_user.id)
        for cart in carts:
            order_detail = db.add_order_detail(order.order_id,cart.cart_book_id,cart.book_num)
            order.order_price += order_detail.orDetail_price
        db.add_order_price(order.order_id,order.order_price)
        return 
    