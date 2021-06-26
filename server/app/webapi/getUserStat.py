from . import *
from datetime import datetime

def cal_score(standard, s):
    for k, v in standard.items():
        if s>=k[0] and s<k[1]:
            return v

class GetUserStat(Resource):
    @auth.login_required
    def get(self):
        precision_stand = {
            (0, 0.9): 0,
            (0.9, 0.91): 1,
            (0.91, 0.92): 2,
            (0.92, 0.93): 3,
            (0.93, 0.94): 4,
            (0.94, 0.95): 5,
            (0.95, 0.96): 6,
            (0.96, 0.97): 7,
            (0.97, 0.98): 8,
            (0.98, 0.99): 9,
        }
        count_standard = {
            (0, 100): 0,
            (100,200):1,
            (200,300):2,
            (300,400):3,
            (400,500):4,
            (500,600):5,
            (600,700):6,
            (700,800):7,
            (800,900):8,
            (900,1000):9,
        }

        time_cost_standard = {
            (0, 0.1):0,
            (0.1, 0.15):1,
            (0.15, 0.2):2,
            (0.2, 0.25):3,
            (0.25, 0.3):4,
            (0.3, 0.35):5,
            (0.35, 0.4):6,
            (0.4, 0.45):7,
            (0.45, 0.5):8,
            (0.5, 0.55):9,
        }
        u = g.user
        average_count = 0 if u.total_record == 0 else u.total_count /u.total_record
        average_time_cost = 0 if u.total_time_cost == 0 else u.total_count / u.total_time_cost
        average_precision = 0 if u.total_count == 0 else 1 - (u.total_mistake / u.total_count)
        count_score = 10 if average_count>1000 else cal_score(count_standard, average_count)
        time_cost_score =  10 if average_time_cost>0.55 else cal_score(time_cost_standard, average_time_cost)
        precision_score = 10 if average_precision>0.99 else cal_score(precision_stand, average_precision)
        score = {
            '篇章长度': count_score,
            '写作时长': time_cost_score,
            '用词正确率': precision_score,
        }

        showInfo = {
            'nickname': u.nickname,
            'time': round(u.total_time_cost/3600,1),
            'count': round(u.total_count/1000, 1),
            'record': u.total_record,
            'num_day': (datetime.now() - u.register_time).days,
        }
        print(showInfo)

        return jsonify(code=200, userStat=score, showInfo=showInfo)
