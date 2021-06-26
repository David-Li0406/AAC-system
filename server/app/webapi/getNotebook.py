from . import *

class GetNotebook(Resource):
    @auth.login_required
    def get(self):
        records = g.user.records
        if not records:
            return jsonify(code=200, message="该用户暂无笔记")
        errorInfo = []
        for record in records:
            correction_collected = CorrectionModel.find_by_collected(record.id)
            for word in correction_collected:
                errorInfo.append({
                    'origin_text_html': word.origin_text_html,
                    'correct_text_html': word.correct_text_html,
                    'context_html': word.context_html,
                    'origin_text': word.origin_text,
                    'correct_text': word.correct_text,
                    'id': word.id,
                })
        return jsonify(code=200,message='返回笔记成功',errorInfo=errorInfo)