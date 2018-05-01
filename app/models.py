#-*- coding:utf-8 -*-
import time
import datetime 
from app import app
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from send_email import send_email
try:
    from sqlalchemy import Column
    from sqlalchemy import Integer,String,Float,DateTime,Boolean,Text,backref
except ImportError:
    print "sqlalchemy library not found"
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
import hashlib  
##-- Basic Table --##
Ser_Collect  = db.Table('Ser_Collect',
    db.Column('user_id',db.Integer,db.ForeignKey('Bas_user.id')),
    db.Column('book_id',db.Integer,db.ForeignKey('Bac_book.book_id')),
    db.Column('cart_time',db.DateTime,default=datetime.datetime.now),
    )

class Cart(db.Model):
    '''收藏表，记录用户和商品之间多对多的关系'''
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
    def __init__(self, activity_name, activity_guest, activity_count, activity_describe,activity_time):
        self.activity_name = activity_name
        self.activity_guest = activity_guest
        self.activity_count = activity_count
        self.activity_describe = activity_describe
        self.activity_time = activity_time
    def __repr__(self):
        return '<Activity : %r>' % self.activity_id        

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
    integral_grade = db.Column(db.String(64))
    integral_score = db.Column(db.Integer)
    def __init__(self, integral_user_id, integral_grade_id, integral_score):
        self.integral_user_id = integral_user_id
        self.integral_grade_id = integral_grade_id
        self.integral_score = integral_score
    def __repr__(self):
        return '<Integral : %r>' % self.integral_id



class Ticket(db.Model):
    '''门票表，记录活动的门票信息'''
    __tablename__ = 'Ser_ticket'
    ticket_id = db.Column(db.Integer, primary_key = True)
    ticket_activity_id = db.Column(db.Integer, primary_key = True)
    ticket_user_id = db.Column(db.Integer)
    ticket_Entry_code = db.Column(db.String(64))
    ticket_status = db.Column(db.String(32))
    def __init__(self, ticket_activity_id, ticket_user_id, ticket_status='pending'):
        self.ticket_user_id = ticket_user_id
        self.ticket_activity_id = ticket_activity_id
        self.ticket_status = ticket_status
        m2 = hashlib.md5()   
        m2.update(src)
        src = srt(ticket_activity_id)+str(ticket_user_id)+str(time.time())
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
    def __init__(self, evaluate_book_id, evaluate_user_id, evaluate_describe, evaluate_score):
        self.evaluate_book_id = evaluate_book_id
        self.evaluate_user_id = evaluate_user_id
        self.evaluate_describe = evaluate_describe
        self.evaluate_score = evaluate_score
    def __repr__(self):
        return '<Evaluate : %r>' % self.evaluate_id

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
        
    def get_classList(self):
        class_list = Classify.query.all()
        return class_list
        
    def get_bookList(self,book_name=""):
        book_name = '%' + book_name + '%'
        books = Book.query.filter(Book.book_name.like(book_name)).all()
        return books
    
    def get_activityList(self,activity_name=""):
        activity_name = '%' + activity_name + '%'
        activitys = Activity.query.filter(Activity.activity_name.like(activity_name)).all()
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
                                        join(Book,Cart.cart_book_id==Book.book_id)

        return books
        
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
            
    def add_activity(self,activity_name,activity_guest,activity_num,activity_message,activity_datetime):
        activity = Activity(activity_name, activity_guest, activity_num, activity_message,activity_datetime)
        try:
            db.session.add(activity)
            db.session.commit()
            return activity.activity_id
        except BaseException,e:
            print e
            return False
            
    def delete_cart(self,user_id):
        carts = Cart.query.filter(Cart.cart_user_id==user_id)
        for cart in carts:
            db.session.delete(cart)
        db.session.commit()
        
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
        