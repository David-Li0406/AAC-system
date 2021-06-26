from . import *

class DeleteUser(Resource):
    @auth.login_required
    def get(self,username):
        u = g.user
        if u.user_type != 'administrator':
            return jsonify(code=401, message="权限不足！")
        user_to_delete = UserModel.find_by_username(username)
        user_to_delete.delete_user()
        return jsonify(code=200, message="删除成功")
