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
        #TODO(caoyue):该程序块，查找所有未举行且开始时间在24h内的活动，通过活动报名人数及可容纳人数
        #判断参与人员，并向参与人员发送入场码邮件
        activitys_p=db.get_activity_query('pending')
        time = datetime.datetime.now() + datetime.timedelta(days = -1)
        for activity in activitys_p:
            if activity.activity_time >= time:
                activity_list=db.get_activity_userquery(activity.activity_id)
                print activity_list
                i=activity.activity_count
                for attach in activity_list:
                    print i
                    if i>0:
                        db.add_ticket(attach.actDetail_activiity_id,attach.actDetail_user_id)
                        db.update_activity_detail(attach.actDetail_activiity_id,attach.actDetail_user_id,'success')
                    else:
                        db.update_activity_detail(attach.actDetail_activiity_id,attach.actDetail_user_id,'faile')
                    i=i-1
                db.update_activity_status(activity.activity_id,'runing')
        activitys_r=db.get_activity_query('runing')
        ####################################################################################################
        #TODO(caoyue):该程序块，查找所有活动时间已过期活动，将其状态修改成完成
        time_now = datetime.datetime.now()
        for activity in activitys_r:
            if time_now >= activity.activity_time:
                db.update_activity_status(activity.activity_id,'success')
        ####################################################################################################
        #TODO(caoyue):该程序块，查找所有用户及其积分，为其修改等级
        ####################################################################################################
if __name__ == '__main__':
    try:
        process()
    except BaseException,e:
        print e
        