#encoding:utf-8
from flask_login import login_required,login_user,logout_user,current_user
import os
import json
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 
from flask_login import login_required
from werkzeug import secure_filename
from app.setting import UPLOAD_FOLDER
import shutil

@app.route('/order/list',methods=['GET','POST'])
@login_required
def order_list():
    '''
    订单列表
    '''
    if request.method == 'GET':
        route = session.get('route')
        #search = request.form['search']
        db = DBOpera()
        orders = db.get_orderList()
        return render_template('manage_orderlist.html',orders=orders)
        
        #TODO(caoyue):在图书表中查找图书


