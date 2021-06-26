from . import *

class PostComment(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未接收到参数")

        content = req.get('content')
        r_id = req.get('record_id')
        is_audio = req.get('is_audio')
        if is_audio:
            c = CommentModel('', g.user.username, r_id, is_audio, content)
        else:
            c = CommentModel(content, g.user.username, r_id)
        c.add_comment()
        r = RecordModel.find_by_id(r_id)
        return jsonify(code=200, message="评论成功！")