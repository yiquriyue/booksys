#-*- coding:utf-8 -*-
import time
import datetime 
import qrcode
from app import app
from flask_login import UserMixin,current_user
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from send_email import send_email
try:
    from sqlalchemy import Column,and_,or_
    from sqlalchemy import Integer,String,Float,DateTime,Boolean,Text,backref
except ImportError:
    print "sqlalchemy library not found"
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
import hashlib  
from setting import QRCODE_FOLDER
##-- Basic Table --##
Ser_Collect  = db.Table('Ser_Collect',
    db.Column('user_id',db.Integer,db.ForeignKey('Bas_user.id')),
    db.Column('book_id',db.Integer,db.ForeignKey('Bac_book.book_id')),
    db.Column('cart_time',db.DateTime,default=datetime.datetime.now),
    )

class Cart(db.Model):
    '''购物车表，记录用户和商品之间多对多的关系'''
    __tablename__ = 'Ser_cart'
    cart_user_id = db.Column(db.Integer,db.ForeignKey('Bas_user.id'),primary_key =True)
    cart_book_id = db.Column(db.Integer,db.ForeignKey('Bac_book.book_id'),primary_key =True)
    cart_time = db.Column(db.DateTime,default=datetime.datetime.now)
    book_num = db.Column(db.Integer, default=1)

    # def __init__(self, collect_book_id,collect_user_id):
        # self.collect_book_id = collect_book_id
        # self.collect_user_id = collect_user_id
        
    def __repr__(self):
        return '<cart_book_id : %r>' % self.cart_book_id
        
class User(UserMixin,db.Model):
    '''用户基本表，记录用户基本信息'''
    __tablename__ = 'Bas_user'
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(128))
    user_phone = db.Column(db.String(11))
    user_password = db.Column(db.String(128))
    user_email = db.Column(db.String(32))
    confirmed = db.Column(db.Boolean,default=False)
    route = db.Column(db.Boolean,default=False)
    Bac_book = db.relationship('Book',secondary=Ser_Collect,
                            backref=db.backref('Bas_user',lazy='dynamic'),
                            lazy='dynamic')
    collect = db.relationship('Cart',
                              foreign_keys=[Cart.cart_user_id],
                              backref=db.backref('Book.collect',lazy='joined'),
                              lazy='dynamic',
                              cascade='all,delete-orphan')
    def __init__(self,user_name,user_phone,user_email):
        self.user_name = user_name
        self.user_phone = user_phone
        self.user_email = user_email
    
    def init_password(self,password):
        self.user_password = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.user_password,password)
        
    def get_confirmation(self ,expiration=3600):
        s= Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})
        
    def confirm(self,token):
        print "comfirm"
        s=Serializer(current_app.config['SECRET_KEY'])
        print token
        try:
            data=s.loads(token)
            print data
        except:
            return False
        print data.get('confirm')
        if data.get('confirm')!=self.id:
            return False
        self.confirmed= True
        db.session.add(self)
        db.session.commit()
        return True
        
    def __repr__(self):
        return '<User : %r>' % self.user_name

class Admin(db.Model):
    '''管理员基本表，记录管理员信息'''
    __tablename__ = 'Bas_admin'
    admin_id = db.Column(db.Integer, primary_key = True)
    admin_name = db.Column(db.String(128))
    admin_phone = db.Column(db.String(11))
    admin_password = db.Column(db.String(64))
    def __init__(self,admin_name,admin_phone,admin_password):
        self.admin_name = admin_name
        self.admin_phone = admin_phone
        self.admin_password = admin_password
    def __repr__(self):
        return '<Admin : %r>' % self.admin_name

class Book(db.Model):
    """书籍基本表，记录书籍的信息"""
    '''
    @param(book_id):图书编号
    @param(book_name):图书名称
    @param(book_author):图书作者
    @param(book_price):图书价格
    @param(book_class):图书类别编号
    @param(book_message):图书描述
    @param(book_class):图书类别编号
    
    '''
    __tablename__ = 'Bac_book'
    book_id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(128))
    book_author = db.Column(db.String(128))
    book_price = db.Column(db.Float)
    book_class = db.Column(db.Integer)
    book_message = db.Column(db.Text)
    book_image = db.Column(db.String(128))
    book_num = db.Column(db.Integer)
    book_time = db.Column(db.DateTime,default=datetime.datetime.now())
    collect = db.relationship('Cart',
                              foreign_keys=[Cart.cart_book_id],
                              backref=db.backref('User.collect',lazy='joined'),
                              lazy='dynamic',
                              cascade='all,delete-orphan')
    def __init__(self, book_name, book_author, book_price,book_class,book_num,book_message = ""):
        self.book_name = book_name
        self.book_author = book_author
        self.book_price = book_price
        self.book_class = book_class
        self.book_message = book_message
        self.book_num = book_num

        
    def __repr__(self):
        return '<Book : %r>' % self.book_name

class Classify(db.Model):
    '''分类表，记录书籍的类别信息'''
    __tablename__ = 'Bas_classify'
    classify_id = db.Column(db.Integer, primary_key = True)
    classify_name = db.Column(db.String(64))
    classify_father = db.Column(db.Integer)
    def __init__(self, classify_name, classify_father):
        self.classify_name = classify_name
        self.classify_father = classify_father
    def __repr__(self):
        return '<Classify : %r>' % self.classify_name

class Activity(db.Model):
    '''活动表，记录讲座沙龙活动的信息'''
    __tablename__ = 'Bas_activity'
    activity_id = db.Column(db.Integer, primary_key = True)
    activity_name = db.Column(db.String(128))
    activity_guest = db.Column(db.String(64))
    activity_count = db.Column(db.Integer)
    activity_describe = db.Column(db.Text)
    activity_time = db.Column(db.DateTime)
    activity_status = db.Column(db.String(16))
    def __init__(self, activity_name, activity_guest, activity_count, activity_describe,activity_time):
        self.activity_name = activity_name
        self.activity_guest = activity_guest
        self.activity_count = activity_count
        self.activity_describe = activity_describe
        self.activity_time = activity_time
        self.activity_status = 'pending'
    def __repr__(self):
        return '<Activity : %r>' % self.activity_id        

        
class Activity_detail(db.Model):
    '''活动详情表，记录参与活动的信息'''
    __tablename__ = 'Bas_activity_detail'
    actDetail_id = db.Column(db.Integer, primary_key = True)
    actDetail_activiity_id = db.Column(db.Integer)
    actDetail_user_id = db.Column(db.Integer)
    actDetail_status = db.Column(db.String(16))
    
    def __init__(self, actDetail_activiity_id,actDetail_user_id, actDetail_status):
        self.actDetail_activiity_id = actDetail_activiity_id
        self.actDetail_user_id = actDetail_user_id
        self.actDetail_status = actDetail_status

    def __repr__(self):
        return '<Activity_detail : %r>' % self.actDetail_id
        
class Order(db.Model):
    '''订单表，记录订单中用户及金额等信息'''
    __tablename__ = 'Bas_order'
    order_id = db.Column(db.Integer, primary_key = True)
    order_user_id = db.Column(db.Integer)
    order_price = db.Column(db.Float)
    order_time = db.Column(db.DateTime,default=datetime.datetime.now())
    order_status = db.Column(db.String(16))
    def __init__(self, order_user_id, order_price, order_status):
        self.order_user_id = order_user_id
        self.order_price = order_price
        self.order_status = order_status
    def __repr__(self):
        return '<Order : %r>' % self.order_id

class Order_detail(db.Model):
    '''订单明细业务表，记录订单中书籍详情'''
    __tablename__ = 'Bas_order_detail'
    orDetail_id = db.Column(db.Integer, primary_key = True)
    orDetail_order_id = db.Column(db.Integer)
    orDetail_book_id = db.Column(db.Integer)
    orDetail_num = db.Column(db.Integer)
    orDetail_price = db.Column(db.Float)
    
    def __init__(self, orDetail_order_id,orDetail_book_id, orDetail_num,orDetail_price):
        self.orDetail_order_id = orDetail_order_id
        self.orDetail_book_id = orDetail_book_id
        self.orDetail_num = orDetail_num
        self.orDetail_price = orDetail_price
    def __repr__(self):
        return '<Order_detail : %r>' % self.orDetail_id

##-- Service Table --##


class Integral(db.Model):
    '''积分业务表，记录用户每类积分'''
    __tablename__ = 'Ser_integral'
    integral_id = db.Column(db.Integer, primary_key = True)
    integral_user_id = db.Column(db.Integer)
    integral_grade = db.Column(db.Integer)
    integral_score = db.Column(db.Integer)
    def __init__(self, integral_user_id, integral_grade_id, integral_score):
        self.integral_user_id = integral_user_id
        self.integral_grade = integral_grade_id
        self.integral_score = integral_score
    def __repr__(self):
        return '<Integral : %r>' % self.integral_id

class Ticket(db.Model):
    '''门票表，记录活动的门票信息'''
    __tablename__ = 'Ser_ticket'
    ticket_id = db.Column(db.Integer, primary_key = True)
    ticket_activity_id = db.Column(db.Integer)
    ticket_user_id = db.Column(db.Integer)
    ticket_Entry_code = db.Column(db.String(64))
    ticket_status = db.Column(db.String(32))
    def __init__(self, ticket_activity_id, ticket_user_id, ticket_status='pending'):
        self.ticket_user_id = ticket_user_id
        self.ticket_activity_id = ticket_activity_id
        self.ticket_status = ticket_status
        m2 = hashlib.md5()   
        src = str(ticket_activity_id)+str(ticket_user_id)+str(time.time())
        m2.update(src)
        self.ticket_Entry_code = m2.hexdigest()
    def __repr__(self):
        return '<Ticket : %r>' % self.ticket_id

class Evaluate(db.Model):
    '''评分表，记录用户对书籍的评价'''
    __tablename__ = 'Ser_evaluate'
    evaluate_id = db.Column(db.Integer, primary_key =True)
    evaluate_book_id = db.Column(db.Integer)
    evaluate_user_id = db.Column(db.Integer)
    evaluate_describe = db.Column(db.Text)
    evaluate_score = db.Column(db.Float)
    evaluate_ststus = db.Column(db.Boolean,default=False)
    evaluate_time = db.Column(db.DateTime,default=datetime.datetime.now)
    def __init__(self, evaluate_book_id, evaluate_user_id, evaluate_describe, evaluate_score):
        self.evaluate_book_id = evaluate_book_id
        self.evaluate_user_id = evaluate_user_id
        self.evaluate_describe = evaluate_describe
        self.evaluate_score = evaluate_score
    def __repr__(self):
        return '<Evaluate : %r>' % self.evaluate_id

class Statics(db.Model):
    '''统计表，用于统计销量，收藏量，等信息'''
    __tablename__ = 'Ser_statics'
    statics_id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.Integer)
    sale_num = db.Column(db.Integer,default=0)
    collect_num = db.Column(db.Integer,default=0)
    def __init__(self,book_id):
        self.book_id = book_id
    def __repr__(self):
        return '<Status : %r>' % self.statics_id
    

class DBOpera():
    def user_check(self,username,password):
        user = User.query.filter_by(user_name = username).first()
        if user:
            if user.verify_password(password):
                return user.id
            else:
                return False
        else:
            return False
    
    def manager_check(self,username,password):
        user = User.query.filter_by(user_name = username).first()
        if user:
            if user.verify_password(password):
                if user.route:
                    return user.id
                else:
                    return False
            else:
                return False
        else:
            return False
    
    def user_register(self,username,password,email,phone):
        user = User(username,phone,email)
        user.init_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            token= user.get_confirmation()
            send_email(user.user_email,'Confirm Your Account','user/confirm_1',user=user,token=token)
            return user.id
        except BaseException,e:
            print e
            return False
    
    def check_evaluate(self,book_id):
        user_id = current_user.id
        evaluate = Evaluate.query.filter_by(evaluate_book_id=book_id,evaluate_user_id=user_id).all()
        if evaluate:
            return  True
        else:
            return False
    
    def get_classList(self):
        class_list = Classify.query.all()
        return class_list
        
    def get_bookList(self,keyword=""):
        keyword = '%' + keyword + '%'
        books = Book.query.filter(or_(Book.book_author.like(keyword),Book.book_name.like(keyword))).all()
        return books
    
    def get_NewBook(self):
        books = Book.query.order_by(Book.book_time.desc()).limit(8)
        return books
    
    def get_bassSaleBook(self):
        books = db.session.query(Book).join(Statics,Statics.book_id==Book.book_id).\
                order_by(Statics.sale_num.desc()).limit(8)
        return books
        
    def get_orderList(self,user_name=""):
        if user_name:
            user = User.query.filter(User.user_name==user_name).first()
            orders = Order.query.filter(Order.order_user_id == user.id,Order.order_status=='obligation').all()
        else:
            orders = Order.query.filter(Order.order_status=='obligation').all()
        return orders
        
    def get_orderPrice(self,order_id):
        order = Order.query.get(order_id)
        return order.order_price
        
    def get_orderUser(self,order_id):
        order = Order.query.get(order_id)
        return order.order_user_id
        
    def get_orderAttach(self,order_id):
        books = db.session.query(Book,Order_detail.orDetail_num).select_from(Order_detail).\
                                    filter_by(orDetail_order_id=order_id).\
                                    join(Book,Order_detail.orDetail_book_id==Book.book_id).all()
        return books
    
    def get_activityList(self,keyword=""):
        keyword = '%' + keyword + '%'
        activitys = Activity.query.filter(or_(Activity.activity_name.like(keyword),Activity.activity_guest.like(keyword)))
        print activitys
        activitys = activitys.all()
        return activitys
        
    def get_NewActivity(self):
        activitys = Activity.query.order_by(Activity.activity_time.desc()).limit(3)
        return activitys
        
    def get_bookAttach(self,book_id):
        book = Book.query.filter(Book.book_id==book_id).first()
        return book
    
    def get_activityAttach(self,activity_id):
        activity = Activity.query.filter(Activity.activity_id==activity_id).first()
        return activity
        
    def get_collect(self,user_id):
        user = User.query.get(user_id)
        carts = user.Bac_book.all()
        return carts
        
    def get_cart(self,user_id):
        books = db.session.query(Book,Cart.book_num).select_from(Cart).\
                                        filter_by(cart_user_id=user_id).\
                                        join(Book,Cart.cart_book_id==Book.book_id).all()
        return books
        
        
        
    def get_confirmUser(self):
        users = User.query.filter(User.confirmed==True).all()
        return users
        
    def get_activity_query(self,status):
        activitys = Activity.query.filter(Activity.activity_status==status).all()
        return activitys
        
    def get_activity_userquery(self,activity_id):
        activity_details = Activity_detail.query.filter(Activity_detail.actDetail_activiity_id==activity_id).all()
        #这里还需要对user进行排序，通过积分，但是积分还没有建立好
        return activity_details
     
    def get_grade_query(self):
        grades = Integral.query.all()
        return grades
    
    def get_integral(self,user_id):
        integral = Integral.query.filter(Integral.integral_user_id==user_id).first()
        return integral
    
    def get_userBoughtBook(self,user_id):
        books = db.session.query(Book).select_from(Order).\
                filter(Order.order_user_id==user_id,Order.order_status=='success').\
                join(Order_detail,and_(Order.order_id==Order_detail.orDetail_order_id)).\
                join(Book,and_(Order_detail.orDetail_book_id==Book.book_id)).all()
                
        return books
        
    def get_evaluate(self,book_id):
        evaluates = Evaluate.query.\
                    filter(Evaluate.evaluate_book_id==book_id).\
                    all()
        return evaluates
        
        
    def add_book(self,book_name,book_author,book_class,
                 book_price,book_num,book_message = ""):
        book = Book(book_name, book_author, book_price,book_class,book_num,book_message)
        try:
            db.session.add(book)
            db.session.commit()
            print book.book_id
            return book.book_id
        except BaseException,e:
            print e
            return False
            

    def add_bookImag(self,book_id,book_image):
        book = Book.query.filter_by(book_id = book_id).first()
        book.book_image = book_image
        try:
            db.session.add(book)
            db.session.commit()
            return book.book_id
        except BaseException,e:
            print e
            return False
            
    def add_collect(self,book_id,user_id):
        book = Book.query.filter_by(book_id = book_id).first()
        user = User.query.filter_by(id = user_id).first()
        user.Bac_book.append(book)
        try:
            db.session.add(user)
            db.session.commit()
            print user
            return True
        except BaseException,e:
            print e
            return False
            

            
    def add_cart(self,book_id,user_id):
        cart=Cart.query.filter(Cart.cart_book_id==book_id,Cart.cart_user_id==user_id).first()
        if cart:
            cart.book_num = cart.book_num +1
            db.session.add(cart)
        else:
            cart_new = Cart(cart_book_id=book_id,cart_user_id=user_id)
            db.session.add(cart_new)
        try:
            db.session.commit()
            print 'cart',cart
        except BaseException,e:
            print e
            return False
            
    def add_order(self,user_id):
        order = Order(user_id,0,'obligation')
        try:
            db.session.add(order)
            db.session.commit()
            return order
        except BaseException,e:
            print e
            return False
            
    def add_order_price(self,order_id,price):
        order = Order.query.get(order_id)
        order.order_price = price
        try:
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
            
    def add_order_detail(self,order_id,book_id,book_num):
        book = Book.query.get(book_id)
        price = book.book_price * book_num
        order_detail = Order_detail(int(order_id),book_id,book_num,price,)
        try:
            db.session.add(order_detail)
            db.session.commit()
            return order_detail
        except BaseException,e:
            print e
            return False
            
    def add_activity_detail(self,activity_id,user_id):
        activity_detail = Activity_detail(int(activity_id),int(user_id),'pending')
        try:
            db.session.add(activity_detail)
            db.session.commit()
            return activity_detail
        except BaseException,e:
            print e
            return False
            
    def add_activity(self,activity_name,activity_guest,activity_num,activity_message,activity_datetime):
        activity = Activity(activity_name, activity_guest, activity_num, activity_message,activity_datetime)
        try:
            db.session.add(activity)
            db.session.commit()
            return activity.activity_id
        except BaseException,e:
            print e
            return False
            
    def add_ticket(self,ticket_activity_id, user_id):
        ticket = Ticket(ticket_activity_id, user_id)
        user = User.query.get(user_id)
        try:
            db.session.add(ticket)
            db.session.commit()
            '''
            #TODO(CAOYUE):这里用来生成二维码，但是PIL和image库没有添加成功，待完善
            img = qrcode.make(ticket.ticket_Entry_code)
            if os.path.exists(os.path.join(QRCODE_FOLDER,ticket.ticket_Entry_code)):
                shutil.rmtree(os.path.join(QRCODE_FOLDER,ticket.ticket_Entry_code))
            os.mkdir(os.path.join(QRCODE_FOLDER,ticket.ticket_Entry_code))
            filename = 'qrcode.jpg'
            qrcode_image = os.path.join(UPLOAD_FOLDER,ticket.ticket_Entry_code,filename)
            img.save(qrcode_image)
            code_imag = 'qrcode/'+ ticket.ticket_Entry_code +'qrcode.jpg'
            send_email(user.user_email,'A ticket','user/ticket',user_name=user.user_name,postcode=ticket.ticket_Entry_code,code_imag=code_imag)
            '''
            send_email(user.user_email,'A ticket','user/ticket',user_name=user.user_name,postcode=ticket.ticket_Entry_code)
            return True
        except BaseException,e:
            print e
            return False
        
    
    def add_evaluate(self,book_id,scort,message):
        evaluate = Evaluate(book_id,current_user.id,message,scort)
        try:
            db.session.add(evaluate)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
    
    def add_integral(self,user_id):
        integral = Integral(user_id,0,0)
        try:
            db.session.add(integral)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
    
    def add_statics(self,book_id):
        statics = Statics(book_id)
        try:
            db.session.add(statics)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
    
    def delete_cart(self,user_id,book_id=""):
        if book_id:
            #DOND(caoyue):用户删除购物车中指定图书
            cart = Cart.query.filter(Cart.cart_book_id==book_id,Cart.cart_user_id==user_id).first()
            db.session.delete(cart)
        else:
            #DOND(caoyue):清空购物车，提交订单后执行该操作
            carts = Cart.query.filter(Cart.cart_user_id==user_id)
            for cart in carts:
                db.session.delete(cart)
        db.session.commit()
        
    def delete_collect(self,user_id,book_id):
        book = Book.query.filter_by(book_id = book_id).first()
        user = User.query.filter_by(id = user_id).first()
        user.Bac_book.remove(book)
        try:
            db.session.add(user)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
        
    def update_activity_detail(self,activity_id,user_id,status):
        activity_detail = Activity_detail.query.filter(Activity_detail.actDetail_activiity_id==activity_id,\
                            Activity_detail.actDetail_user_id==user_id).first()
        activity_detail.actDetail_status = status
        try:
            db.session.add(activity_detail)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
            
    def update_activity_status(self,activity_id,status):
        activity = Activity.query.get(activity_id)
        activity.activity_status = status
        try:
            db.session.add(activity)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
            
    def update_user(self,password,email,phone):
        user = User.query.get(current_user.id)
        user.user_password = generate_password_hash(password)
        user.user_email = email
        user.user_phone = phone
        user.confirmed = False
        try:
            db.session.add(user)
            db.session.commit()
            token= user.get_confirmation()
            send_email(user.user_email,'Confirm Your Account','user/confirm_1',user=user,token=token)
            return True
        except BaseException,e:
            print e
            return False
    
    def update_book(self,book_id,book_name,book_author,book_class,book_message,book_num,book_price):
        book = Book.query.get(book_id)
        book.book_name = book_name
        book.book_author = book_author
        book.book_class = book_class
        book.book_message = book_message
        book.book_num = book_num
        book.book_price = book_price
        try:
            db.session.add(book)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
    
    def update_book_num(self,book_id,num,opera):
        book = Book.query.get(book_id)
        if opera=='+':
            book.book_num = book.book_num + num
        elif opera == '-':
            book.book_num = book.book_num - num
        try:
            db.session.add(book)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
    def update_order_status(self,order_id):
        order = Order.query.filter(Order.order_id==order_id).first()
        order.order_status = 'success'
        orderDtls = Order_detail.query.filter(Order_detail.orDetail_order_id==order_id).all()
        for orderDtl in orderDtls:
            self.update_book_num(orderDtl.orDetail_book_id,orderDtl.orDetail_num,'-')
            self.update_statics(orderDtl.orDetail_book_id,orderDtl.orDetail_num)
        try:
            db.session.add(order)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
    
    def update_activity(self,activity_id,activity_name,activity_guest,activity_num,activity_message,activity_datetime):
        activity = Activity.query.get(activity_id)
        activity.activity_name = activity_name
        activity.activity_guest = activity_guest
        activity.activity_num = activity_num
        activity.activity_message = activity_message
        activity.activity_datetime = activity_datetime
        try:
            db.session.add(activity)
            db.session.commit()
            return True
        except BaseException,e:
            print e
            return False
    def update_ticket(self,activity_id):
        tickets = Ticket.query.filter(Ticket.ticket_activity_id==activity_id,Ticket.ticket_status=='pending').first()
        for ticket in tickets:
            ticket.ticket_status='failure'
            self.minus_integral(ticket.ticket_user_id,30)
            db.session.add(ticket)
            db.session.commit()
            return ticket.ticket_user_id
        else:
            return False
    def update_integral(self,user_id,num):
        integral = Integral.query.filter(Integral.integral_user_id==user_id).first()
        if integral:
            integral.integral_score = integral.integral_score + num
            try:
                db.session.add(integral)
                db.session.commit()
                return True
            except:
                return False
    
    def update_integral_grade(self,user_id,status):
        integral = Integral.query.filter(Integral.integral_user_id==user_id).first()
        if integral:
            integral.integral_grade = status
            try:
                db.session.add(integral)
                db.session.commit()
                return True
            except:
                return False
    
    def update_grade_num(self,user_id,num):
        integrals = Integral.query.\
                   order_by(Integral.integral_grade.desc()).limit(num)
        integral_user = Integral.query.filter(Integral.integral_user_id==user_id).first()
        if integral_user in integrals:
            return True
        else :
            return False
    
    def update_statics(self,book_id,sale_num=0,collect_num=0):
        statics = Statics.query.filter(Statics.book_id==book_id).first()
        if not statics:
            statics = Statics(book_id)
            try:
                db.session.add(statics)
                db.session.commit()
            except:
                return False
        statics.sale_num = statics.sale_num + sale_num
        statics.collect_num = statics.collect_num + collect_num
        try:
            db.session.add(statics)
            db.session.commit()
            return True
        except:
            return False
        
    def minus_integral(self,user_id,num):
        integral = Integral.query.filter(Integral.integral_user_id==user_id).first()
        if integral:
            integral.integral_score = integral.integral_score - num
            try:
                db.session.add(integral)
                db.session.commit()
                return True
            except:
                return False
                
                
    def ticket_check(self,postcode):
        ticket = Ticket.query.filter(Ticket.ticket_Entry_code==postcode,Ticket.ticket_status=='pending').first()
        if ticket:
            ticket.ticket_status='success'
            db.session.add(ticket)
            db.session.commit()
            return ticket.ticket_user_id
        else:
            return False
@login_manager.user_loader
def get_userinfo(userId):
    user = User.query.filter(User.id==userId).first()
    return user
#db.create_all()
#db.drop_all()
if __name__ == '__main__':
    try:
        db.create_all()
        #db.drop_all()
        print "database create success"
    except BaseException,e:
        print "000000"
        print e
        