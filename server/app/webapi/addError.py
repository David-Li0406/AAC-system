from . import *

class AddError(Resource):
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未收到参数")
        id = req.get('id')
        c = CorrectionModel.find_by_id(id)
        c.collected = True
        db.session.commit()
        return jsonify(code=200, message='添加成功')