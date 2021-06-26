from . import *

class GetUser(Resource):
    @auth.login_required
    def get(self,page):
        u = g.user
        if u.user_type != 'administrator':
            return jsonify(code=401, message="权限不足！")
        u_page = UserModel.find_all_user(page)
        retInfo = []
        for u in u_page.items:
            print(u.username)
            recordInfo = {
                'register_time': '2021/5/12',
                'username': u.username,
                'email': u.email,
                'total_record': u.total_record,
            }
            retInfo.append(recordInfo)
        if page == 1:    
            return jsonify(code=200, message='返回成功', retInfo=retInfo, total=u_page.total)
        return jsonify(code=200, message='返回成功', retInfo=retInfo)
        