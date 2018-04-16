#-*- coding:utf-8 -*-
from __init__ import db
from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
try:
	from sqlalchemy import Column
	from sqlalchemy import Integer,String,Float,DateTime,Boolean
except ImportError:
	print "sqlalchemy library not found"
##-- Basic Table --##
class User(db.Model):
	'''用户基本表，记录用户基本信息'''
	__tablename__ = 'Bas_user'
	user_id = db.Column(db.Integer, primary_key = True)
	user_name = db.Column(db.String(128))
	user_phone = db.Column(db.String(11))
	user_password = db.Column(db.String(64))
	user_email = db.Column(db.String(32))

	def __init__(self,user_name,user_phone,user_password,user_email):
		self.user_name = user_name
		self.user_phone = user_phone
		self.user_password = user_password
		self.user_email = user_email

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
	__tablename__ = 'Bac_book'
	book_id = db.Column(db.Integer, primary_key = True)
	book_name = db.Column(db.String(128))
	book_author = db.Column(db.String(128))
	book_price = db.Column(db.Integer)
	book_class = db.Column(db.Integer)

	def __init__(self, book_name, book_author, book_price,book_class):
		self.book_name = book_name
		self.book_author = book_author
		self.book_price = book_price
		self.book_class = book_class
	def __repr__(self):
		return '<Book : %r>' % self.book_name

class BookShelf(db.Model):
	"""书架表，记录书架信息"""
	__tablename__ = 'Bas_bookshelf'
	shelf_id = db.Column(db.Integer, primary_key = True)
	shelf_name = db.Column(db.String(32))
	def __init__(self, shelf_name):
		self.shelf_name = shelf_name
	def __repr__(self):
		return '<BookShelf : %r>' % self.shelf_name

class Grade(db.Model):
	'''等级表，记录等级信息'''
	__tablename__ = 'Bas_grade'
	grade_id = db.Column(db.Integer, primary_key = True)
	grade_name = db.Column(db.String(64))
	def __init__(self, grade_name):
		self.grade_name = grade_name
	def __repr__(self):
		return '<Grade : %r>' % self.grade_name

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
	


##-- Service Table --##
class Order(db.Model):
	'''订单业务表，记录订单中用户及金额等信息'''
	__tablename__ = 'Ser_order'
	order_id = db.Column(db.Integer, primary_key = 	True)
	order_user_id = db.Column(db.Integer)
	order_price = db.Column(db.Float)
	order_time = db.Column(db.DateTime)
	order_status = db.Column(db.String(16))
	order_address_id = db.Column(db.Integer)
	def __init__(self, order_user_id, order_price, order_time, order_status, order_address_id):
		self.order_user_id = order_user_id
		self.order_price = order_price
		self.order_time = order_time
		self.order_status = order_status
		self.order_address_id = order_address_id
	def __repr__(self):
		return '<Order : %r>' % self.order_id

class Order_detail(db.Model):
	'''订单明细业务表，记录订单中书籍详情'''
	__tablename__ = 'Ser_order_detail'
	orDetail_id = db.Column(db.Integer, primary_key = True)
	orDetail_order_id = db.Column(db.Integer, primary_key = True)
	orDetail_book_id = db.Column(db.Integer)
	orDetail_num = db.Column(db.Integer)
	def __init__(self, orDetail_book_id, orDetail_num):
		self.orDetail_id = orDetail_id
		self.orDetail_num = orDetail_num
	def __repr__(self):
		return '<Order_detail : %r>' % self.orDetail_id

class Integral(db.Model):
	'''积分业务表，记录用户每类积分'''
	__tablename__ = 'Ser_integral'
	integral_id = db.Column(db.Integer, primary_key = True)
	integral_user_id = db.Column(db.Integer)
	integral_grade_id = db.Column(db.Integer)
	integral_score = db.Column(db.Integer)
	def __init__(self, integral_user_id, integral_grade_id, integral_score):
		self.integral_user_id = integral_user_id
		self.integral_grade_id = integral_grade_id
		self.integral_score = integral_score
	def __repr__(self):
		return '<Integral : %r>' % self.integral_id

class Activity(db.Model):
	'''活动表，记录讲座沙龙活动的信息'''
	__tablename__ = 'Ser_activity'
	activity_id = db.Column(db.Integer, primary_key = True)
	activity_name = db.Column(db.String(128))
	activity_guest = db.Column(db.String(64))
	activity_count = db.Column(db.Integer)
	activity_describe = db.Column(db.Text)
	def __init__(self, activity_name, activity_guest, activity_count, activity_describe):
		self.activity_name = activity_name
		self.activity_guest = activity_guest
		self.activity_count = activity_count
		self.activity_describe = activity_describe
	def __repr__(self):
		return '<Activity : %r>' % self.activity_id

class Ticket(db.Model):
	'''门票表，记录活动的门票信息'''
	__tablename__ = 'Ser_ticket'
	ticket_id = db.Column(db.Integer, primary_key = True)
	ticket_activity_id = db.Column(db.Integer, primary_key = True)
	ticket_user_id = db.Column(db.Integer)
	ticket_seat = db.Column(db.Integer)
	def __init__(self, ticket_activity_id, ticket_user_id, ticket_seat):
		self.ticket_user_id = ticket_user_id
		self.ticket_activity_id = ticket_activity_id
		self.ticket_seat = ticket_seat
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
			if user.user_password == password:
				return user.user_id
			else:
				return False
		else:
			return False

	def user_register(self,username,password,email,phone):
		user = User(username,phone,password,email)
		try:
			db.session.add(user)
			db.session.commit()
			return user.user_id
		except BaseException,e:
			print e
			return False

	def get_userinfo(self,userId):
		user = User.query.filter(User.user_id==userId).first()
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