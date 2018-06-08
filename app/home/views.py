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
from app.models import DBOpera 

@app.route('/home',methods=['GET','POST'])
def home():
    '''
    用户主页
    '''
    if request.method == 'GET':
        db = DBOpera()
        # DONE(CAOYUE):最新图书
        new_books = db.get_NewBook()
        new_book_list = []
        for book in new_books:
            abook={}
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
            new_book_list.append(abook)
        # DONE(CAOYUE):最新活动
        new_activitys = db.get_NewActivity()
        now_activity_list = []
        for activity in new_activitys:
            a_activity = {}
            a_activity['id'] = activity.activity_id
            a_activity['name'] = activity.activity_name
            a_activity['guest'] = activity.activity_guest
            a_activity['describe'] = activity.activity_describe
            now_activity_list.append(a_activity)
        # TODO(CAOYUE):最热图书
        bass_sale = db.get_bassSaleBook()
        bassSale_book_list = []
        for book in bass_sale:
            abook={}
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
            bassSale_book_list.append(abook)
        try:
            search = request.args['search']
        except:
            search = None
        if search :
            return redirect(url_for('book_list',search=search))
        else :
            return render_template('user_index.html',new_book=new_book_list,new_activity=now_activity_list,baseSale_book=bassSale_book_list)