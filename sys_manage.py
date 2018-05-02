from app.models import DBOpera
import datetime
def process():
    db = DBOpera()
    while 1:
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
        time_now = datetime.datetime.now()
        for activity in activitys_r:
            if time_now >= activity.activity_time:
                db.update_activity_status(activity.activity_id,'success')
if __name__ == '__main__':
    try:
        process()
    except BaseException,e:
        print e
        