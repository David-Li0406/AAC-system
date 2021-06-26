from . import *

class CheckUserApi(Resource):

    def post(self):
        req = request.json

        # 检查用户名是否已注册
        user = UserModel.find_by_username(req.get("username"))
        if user:
            return jsonify(code=403, wrongType="username", message="用户名已被注册")

        return jsonify(code=200, message="用户名可注册！")