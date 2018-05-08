#encoding:utf-8
#from app.models import User
from flask_login import login_required,login_user,logout_user,current_user
import os
# from . import auth
from flask import request,render_template,flash,abort,url_for,redirect,session,Flask,g
from app import app
from app.models import DBOpera 
from app.send_email import send_email
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
            return render_template('manage_activitylist.html',activity_list=activity_list)
    if request.method == 'POST':
        route = session.get('route')
        #search = request.form['search']
        db = DBOpera()
        keyword = request.form['keyword']
        activitys = db.get_activityList(keyword)
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
            return render_template('manage_activitylist.html',activity_list=activity_list)

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
        activity_datetime = request.form['activity_datetime']
        print activity_datetime
        activity_num = int(activity_num)
        activity_id = db.add_activity(activity_name,activity_guest,activity_num,activity_message,activity_datetime)
        #TODO(caoyue):when add a new activity,we send a email to user who have confirm
        users = db.get_confirmUser()
        for user in users:
            send_email(user.user_email,'A new activity looks forward to your participation.','user/activity',user=user,\
                       time=activity_datetime,guest=activity_guest,activity_id=activity_id)
        return redirect(url_for('activity_add'))
        
@app.route('/activity/confirm',methods=['GET','POST'])
def activity_confirm():
    '''
    验证入场码
    '''
    db = DBOpera()
    if request.method == 'GET':
        return render_template('manage_activityconfirm.html')
    if request.method =='POST':
        postcode = request.form['postcode']
        if db.ticket_check(postcode):
            pass
            #验证成功，需要加成功提示在前端
        else:
            pass
            #验证失败，需要加失败提示在前端
        return redirect(url_for('activity_confirm'))
    
    
@app.route('/activity/apply',methods=['GET','POST'])
def activity_apply():
    '''
    用户参与活动，生成添加活动详情
    '''
    if request.method == 'POST':
        activity_id = request.form['activity_id']
        db = DBOpera()
        print activity_id,current_user.id
        db.add_activity_detail(activity_id,current_user.id)
        return redirect(url_for('activity_detail',activity_id=activity_id))
        
@app.route('/activity/update/<activity_id>',methods=['GET','POST'])
def activity_update(activity_id):
    db = DBOpera()
    if request.method == 'GET':
        activity = db.get_activityAttach(activity_id)
        time = activity.activity_time.strftime("%Y-%m-%dT%H:%M:%S")

        return render_template('manage_activityupdate.html',activity=activity,time=time)
    if request.method == 'POST':
        activity_name = request.form['activity_name']
        activity_guest = request.form['activity_guest']
        activity_num = request.form['activity_num']
        activity_message = request.form['activity_message']
        activity_datetime = request.form['activity_datetime']
        activity_num = int(activity_num)
        activity_id = db.update_activity(activity_id,activity_name,activity_guest,activity_num,activity_message,activity_datetime)
        #TODO(caoyue):when add a new activity,we send a email to user who have confirm
        users = db.get_confirmUser()
        for user in users:
            send_email(user.user_email,'A new activity looks forward to your participation.','user/activity_update',
                        user=user,activity_name=activity_name,activity_id=activity_id)
        return redirect(url_for('activity_list'))
    