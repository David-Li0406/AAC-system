from . import *

class GetUserInfo(Resource):
    @auth.login_required
    def get(self, username):
        print(username)
        u = UserModel.find_by_username(username)
        post = 0 if u.records == None else len(u.records) 
        comment = 0 if u.comments == None else len(u.comments)
        reply = 0 if u.replys == None else len(u.replys)
        total_reply = comment+reply
        print(post, total_reply)
        return jsonify(code=200, message='返回成功', post=post, total_reply=total_reply)