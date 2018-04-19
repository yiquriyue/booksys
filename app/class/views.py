#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 

from werkzeug import secure_filename
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
from app.setting import UPLOAD_FOLDER


@app.route('/class/add',methods=['GET','POST'])
def class_add():
    if request.method == 'GET':
        
        #TODO(caoyue):在图书表中查找图书
                               

        