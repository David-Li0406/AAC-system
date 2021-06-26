from . import *

class RegisterApi(Resource):

    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未收到参数")

        # 检查验证码是否正确
        vc = VerificationCodeModel.find_by_email(req.get("email"))
        if vc:
            if vc.code != req.get("verificationCode"):
                return jsonify(code=403, wrongType="verificationCode", message="验证码不正确！")
        else:
            return jsonify(code=403, wrongType="verificationCode", message="验证码不存在！")

        username = req.get('username')
        email = req.get('email')
        password = req.get('password')
        nickname = req.get('nickname')
        u = UserModel(username=username, email=email, nickname=nickname)
        # 单独设置密码（调用加密函数）
        u.password = password

        u.add_user()

        return jsonify(code=200, message="注册成功！")