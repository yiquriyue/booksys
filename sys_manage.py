#-*- coding:utf-8 -*-
from app.models import DBOpera
import datetime
def process():
    '''
    该程序用来循环执行系统操作
    '''
    db = DBOpera()
    #TODO(caoyue):确保程序持续循环运行
    while 1:
        ###############################################################################################
        #DONE(caoyue):该程序块，查找所有未举行且开始时间在24h内的活动，通过活动报名人数及可容纳人数
        #判断参与人员，并向参与人员发送入场码邮件
        try:
            activitys_p=db.get_activity_query('pending')
            time = datetime.datetime.now() + datetime.timedelta(days = -1)
            if activitys_p:
                for activity in activitys_p:
                    if activity.activity_time >= time:
                        activity_list=db.get_activity_userquery(activity.activity_id)
                        print activity_list
                        i=activity.activity_count
                        for attach in activity_list:
                            # print i
                            if i>0:
                                db.add_ticket(attach.actDetail_activiity_id,attach.actDetail_user_id)
                                db.update_activity_detail(attach.actDetail_activiity_id,attach.actDetail_user_id,'success')
                            else:
                                db.update_activity_detail(attach.actDetail_activiity_id,attach.actDetail_user_id,'faile')
                            i=i-1
                        db.update_activity_status(activity.activity_id,'runing')
        except BaseException,e:
            print 1,e
        ####################################################################################################
        #DONE(caoyue):该程序块，查找所有活动时间已过期活动，将其状态修改成完成
        #             并将过期活动的未认证门票状态改为失败，为该门票这人扣除相应积分
        try:
            activitys_r=db.get_activity_query('runing')
            time_now = datetime.datetime.now()
            if activitys_r:
                for activity in activitys_r:
                    if time_now >= activity.activity_time:
                        db.update_activity_status(activity.activity_id,'success')
                        db.update_ticket(activity.activity_id)
        except BaseException,e:
            print 2,e
        ####################################################################################################
        #TODO(caoyue):该程序块，查找所有用户及其积分，为其修改等级
        try:
            grades = db.get_grade_query()
            if grades:
                for grade in grades:
                    if grade.integral_score >= 100:
                        if grade.integral_score >= 1000:
                            if db.update_grade_num(grade.integral_user_id,500):
                                if db.update_grade_num(grade.integral_user_id,100):
                                    if db.update_grade_num(grade.integral_user_id,30):
                                        if db.update_grade_num(grade.integral_user_id,20):
                                            if db.update_grade_num(grade.integral_user_id,10):
                                                if db.update_grade_num(grade.integral_user_id,3):
                                                    if db.update_grade_num(grade.integral_user_id,2):
                                                        if db.update_grade_num(grade.integral_user_id,1):
                                                            db.update_integral_grade(grade.integral_user_id,10)
                                                        else:
                                                            db.update_integral_grade(grade.integral_user_id,9)
                                                    else:
                                                        db.update_integral_grade(grade.integral_user_id,8)
                                                else:
                                                    db.update_integral_grade(grade.integral_user_id,7)
                                            else:
                                                db.update_integral_grade(grade.integral_user_id,6)
                                        else:
                                            db.update_integral_grade(grade.integral_user_id,5)
                                    else:
                                        db.update_integral_grade(grade.integral_user_id,4)
                                else:
                                    db.update_integral_grade(grade.integral_user_id,3)
                            else:
                                db.update_integral_grade(grade.integral_user_id,2)
                        else:
                            db.update_integral_grade(grade.integral_user_id,1)
                    else:
                        db.update_integral_grade(grade.integral_user_id,0)
        except BaseException,e:
            print 3,e
        ####################################################################################################
if __name__ == '__main__':
    try:
        process()
    except BaseException,e:
        print e
        