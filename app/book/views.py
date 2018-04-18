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
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/book/list',methods=['GET','POST'])
def book_list():
    if request.method == 'GET':
        db = DBOpera()
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
        book_id = db.add_book(book_name,book_author,book_class,book_price,book_message)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            book_image = os.path.join(app.config['UPLOAD_FOLDER'], book_id,filename)
            file.save(book_image)
            db.add_bookImag(book_id,book_image)
        return redirect(url_for('book_add'))
@app.route('/book/select',methods=['POST'])
def book_select():
    if request.method == 'POST':
        bookname = request.form['bookname']
        bookathor = request.form['bookathor']
        