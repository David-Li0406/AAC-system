from . import *

class GetHistoryApi(Resource):
    @auth.login_required
    def get(self):
        records = g.user.records
        if not records:
            return jsonify(code=200, message="该用户无评分记录")
        record_data=[]
        for record in records:
            record_data.append({
                'commit_time': str(record.commit_time),
                'article_title': record.article_title,
                'article_content': record.article_content,
                'article_count': record.article_count,
                'article_time_cost': record.article_time_cost,
                'id': record.id
            })
        print(record_data)
        return jsonify(code=200, message="查找成功", records=record_data)