from . import *

class CheckEmailApi(Resource):

    def post(self):
        req = request.json

        # 检查邮箱是否已注册
        user = UserModel.find_by_email(req.get("email"))
        if user:
            return jsonify(code=403, wrongType="email", message="邮箱已被注册")

        return jsonify(code=200, message="邮箱可注册！")