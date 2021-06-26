from . import *

class StarPost(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未收到参数")
        record_id = req.get('record_id')
        r = RecordModel.find_by_id(record_id)
        r.star += 1
        db.session.commit()
        return jsonify(code=200, message="点赞成功")


class StarComment(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未收到参数")
        comment_id = req.get('comment_id')
        c = CommentModel.find_by_id(comment_id)
        c.add_star()
        return jsonify(code=200, message="点赞成功")

class PostReply(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未收到参数")
        username = req.get('username')
        content = req.get('reply_content')
        comment_id = req.get('comment_id')
        record_id = req.get('record_id')

        r = ReplyModel(record_id, comment_id, g.user.username, username, content)
        r.add_reply()
        return jsonify(code=200, message='回复成功')