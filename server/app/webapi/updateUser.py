from . import *

class UpdateUser(Resource):
    @auth.login_required
    def get(self,username):
        u = g.user
        if u.user_type != 'administrator':
            return jsonify(code=401, message="权限不足！")
        user_to_update = UserModel.find_by_username(username)
        user_to_update.set_administrator()
        return jsonify(code=200, message="设置成功！")