from . import *

class MakePublic(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未收到参数")
        id = req.get('id')
        r = RecordModel.find_by_id(id)
        if not r:
            return jsonify(code=404, message='无效的作文id')
        r.public = True
        r.add_record()
        return jsonify(code=200, message="公开成功")