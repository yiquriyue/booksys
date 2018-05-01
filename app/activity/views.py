#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 

@app.route('/activity/list',methods=['GET','POST'])
def activity_list():
    '''
    列出所有活动
    '''
    if request.method == 'GET':
        route = session.get('route')
        #search = request.form['search']
        db = DBOpera()
        activitys = db.get_activityList()
        activity_list = []
        a=1
        for activity in activitys:
            the_activity={}
            the_activity['id'] = str(activity.activity_id)
            the_activity['name'] = activity.activity_name
            the_activity['guest'] = activity.activity_guest
            the_activity['describe'] = activity.activity_describe
            the_activity['time'] = activity.activity_time
            the_activity['count'] = activity.activity_count
            activity_list.append(the_activity)
        if route=='user':
            return render_template('user_blog.html',activity_list=activity_list)
        else:
            return render_template('manage_booklist.html',activity_list=activity_list)
        
        #TODO(caoyue):在图书表中查找图书

@app.route('/activity/detail/<activity_id>',methods=['POST','GET','PUT'])
def activity_detail(activity_id):
    '''
    活动详情
    '''
    if request.method == 'GET':
        db = DBOpera()
        activity = db.get_activityAttach(activity_id)
        return render_template('user_blog_post.html',activity=activity)

@app.route('/activity/add',methods=['GET','POST'])
def activity_add():
    '''
    活动发布
    '''
    db = DBOpera()
    if request.method == 'GET':
        return render_template('manage_activityAdd.html')
    if request.method =='POST':
        activity_name = request.form['activity_name']
        activity_guest = request.form['activity_guest']
        activity_num = request.form['activity_num']
        activity_message = request.form['activity_message']
        activity_datetime = request.files['activity_datetime']
        print activity_datetime
        activity_num = int(activity_num)
        activity_id = db.add_activity(activity_name,activity_guest,activity_num,activity_message,activity_datetime)
        return redirect(url_for('activity_add'))