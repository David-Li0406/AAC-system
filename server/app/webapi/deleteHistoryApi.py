from . import *

class DeleteHistoryApi(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未接收到参数")
        article_id = req.get("id")
        r = RecordModel.find_by_id(article_id)
        r.delete_record()
        return jsonify(code=200, message="删除成功")
        