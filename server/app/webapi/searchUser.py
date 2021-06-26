from . import *

class SearchUser(Resource):
    @auth.login_required
    def get(self,username):
        u = g.user
        if u.user_type != 'administrator':
            return jsonify(code=401, message="权限不足！")
        user_to_search = UserModel.find_by_username(username)
        if not user_to_search:
            return jsonify(code=404,message="没有找到该用户")
        retInfo = []
        userInfo = {
            'register_time': '2021/5/12',
            'username': user_to_search.username,
            'email': user_to_search.email,
            'total_record': user_to_search.total_record,
        }
        retInfo.append(userInfo)
        return jsonify(code=200, retInfo=retInfo, message="查找成功！")