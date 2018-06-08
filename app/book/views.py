#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
import json
import time
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
def book_list():
    '''
    图书列表
    '''
    if request.method == 'GET':
        route = session.get('route')
        try:
            search = request.args['search']
        except:
            search = None
        db = DBOpera()
        if search:
            books = db.get_bookList(search)
        else:
            books = db.get_bookList()
        book_list = []
        a=1
        #TODO(caoyue):书本信息的列表统计
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
        if not route or route=='user':
            return render_template('user_catalog_list.html',book_list=book_list)
        else:
            return render_template('manage_booklist.html',book_list=book_list,book_list1=str(book_list))
    if request.method == 'POST':
        route = session.get('route')
        keyword = request.form['keyword']
        db = DBOpera()
        books = db.get_bookList(keyword)
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
            return render_template('manage_booklist.html',book_list=book_list,book_list1=str(book_list))
        
        
        #TODO(caoyue):在图书表中查找图书
        
                               
@app.route('/book/add',methods=['GET','POST'])
@login_required
def book_add():
    '''
    图书入库
    '''
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
        db.add_statics(book_id)
        if file and allowed_file(file.filename):
            if not os.path.exists(os.path.join(UPLOAD_FOLDER,str(book_id))):
                os.mkdir(os.path.join(UPLOAD_FOLDER,str(book_id)))
            buddha = str(time.time())
            filename = buddha + '.' + file.filename.rsplit('.', 1)[1]
            book_image = os.path.join(UPLOAD_FOLDER,str(book_id),filename)
            fp = open(book_image,'w')
            file.save(book_image)
            fp.close()
            db.add_bookImag(book_id,filename)
        return redirect(url_for('book_add'))

@app.route('/book/detail/<book_id>',methods=['POST','GET','PUT'])
def book_detail(book_id):
    '''
    图书详情
    '''
    if request.method == 'GET':
        db = DBOpera()
        book = db.get_bookAttach(book_id)
        #########################图书信息字典###################################
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
        ########################################################################
        evaluates = db.get_evaluate(book_id)
        evaluate_list = []
        if evaluates:
            for evaluate in evaluates:
                evaluate_dict = {}
                evaluate_dict['user_name'] = evaluate.evaluate_user_id
                evaluate_dict['datatime'] = evaluate.evaluate_time
                evaluate_dict['message'] = evaluate.evaluate_describe
                score = int(evaluate.evaluate_score)
                list0=[]
                list1=[]
                for i in range(score):
                    list0.append(i)
                for i in range(10-score):
                    list1.append(i)
                evaluate_dict['score'] = list0
                evaluate_dict['no_score'] = list1
                evaluate_list.append(evaluate_dict)
        #print evaluate_list
        return render_template('user_product_page.html',book=abook,evaluates=evaluate_list)

        
@app.route('/book/collect/<book_id>',methods=['GET','POST'])
@login_required
def book_collect(book_id):
    '''
    用户添加收藏夹
    '''
    if request.method == 'GET':
        db = DBOpera()
        db.add_collect(book_id,current_user.id)
        return "success"
        
        
@app.route('/book/cart/<book_id>',methods=['GET','POST'])
@login_required
def book_cart(book_id):
    '''
    用户添加购物车
    '''
    if request.method == 'GET':
        db = DBOpera()
        db.add_cart(book_id,current_user.id)
        return "success"

@app.route('/book/cart_delete/<book_id>',methods=['GET','POST'])
@login_required
def book_cart_delete(book_id):
    '''
    用户删除购物车商品
    '''
    if request.method == 'GET':
        db = DBOpera()
        db.delete_cart(current_user.id,book_id)
        return redirect(url_for('cart'))

@app.route('/book/collect_delete/<book_id>',methods=['GET','POST'])
@login_required
def book_collect_delete(book_id):
    '''
    用户删除收藏夹商品
    '''
    if request.method == 'GET':
        #book_id = request.form['book_id']
        db = DBOpera()
        db.delete_collect(current_user.id,book_id)
        return redirect(url_for('collect'))
        
@app.route('/book/add_detail',methods=['GET','POST'])
@login_required
def add_detail():
    '''
    用户提交订单
    '''
    if request.method=='POST':
        books_id = str(request.form['books_id'])
        #数据库操作生成订单，返回订单编号
        books_id = books_id.replace('\'', '\"')
        book_id = json.loads(books_id)
        db = DBOpera()
        order = db.add_order(current_user.id)
        for book in book_id:
            order_detail = db.add_order_detail(str(order.order_id),int(book['book_id']),int(book['book_num']))
            order.order_price += order_detail.orDetail_price
        db.add_order_price(str(order.order_id),order.order_price)
        db.delete_cart(current_user.id)
        return redirect(url_for('cart',status = 1))
        
@app.route('/book/update/<book_id>',methods=['GET','POST'])
@login_required
def book_update(book_id):
    db = DBOpera()
    if request.method == 'GET':
        book = db.get_bookAttach(book_id)
        class_list = db.get_classList()
        return render_template('manage_updatebook.html',book=book,class_list=class_list)
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        book_price = request.form['book_price']
        book_class = request.form['book_class']
        book_message = request.form['book_message']
        file = request.files['book_image']
        book_num = request.form['book_num']
        db.update_book(book_id,book_name,book_author,book_class,book_message,book_num,book_price)
        if file and allowed_file(file.filename):
            try:
                if not os.path.exists(os.path.join(UPLOAD_FOLDER,str(book_id))):
                    os.mkdir(os.path.join(UPLOAD_FOLDER,str(book_id)))
                buddha = str(time.time())
                filename = buddha + '.' + file.filename.rsplit('.', 1)[1]
                book_image = os.path.join(UPLOAD_FOLDER,str(book_id),filename)
                fp = open(book_image,'w')
                file.save(book_image)
                fp.close()
                db.add_bookImag(book_id,filename)
            except BaseException,e:
                print e
        return redirect(url_for('book_list'))

@app.route('/book/evaluate/<book_id>',methods=['GET','POST'])
@login_required
def book_evaluate(book_id):
    db = DBOpera()
    if request.method == 'GET':
        if db.check_evaluate(book_id):
            return redirect(url_for('bookshelf'))
        else:
            return render_template('user_evaluate.html')
    if request.method == 'POST':
        scort = request.form['scort']
        message = request.form['message']
        db.add_evaluate(book_id,scort,message)
        db.update_integral(current_user.id,5)
        return redirect(url_for('book_list'))
