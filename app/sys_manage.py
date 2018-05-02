from models import DBOpera
import datetime
def processs():
    db = DBOpera()
    while 1:
        activitys=db.get_actovity_query()
        time = datetime.datetime.now() + datetime.timedelta(days = -1)
        for activity in activitys:
            if activity.activity_time >= time:
                activity_list=db.get_activity_userquery(activity.activity_id)
                for attact in activity_list:
                    db.add_ticket(attach.actDetail_activiity_id,attach.actDetail_user_id)
                