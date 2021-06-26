from . import *

class Post(Resource):
    def get(self, record_id):
        r = RecordModel.find_by_id(record_id)
        recordInfo = {
            'title': r.article_title,
            'content': r.article_content,
            'commit_time': str(r.commit_time),
            'username': r.user.username,
            'record_id': r.id,
            'star': r.star,
            'view': r.view,
        }
        replys = 0 if r.replys == None else len(r.replys)
        comments = 0 if r.comments == None else len(r.comments)
        recordInfo['total_comment']=replys+comments
        return jsonify(code=200, message='返回成功', recordInfo = recordInfo)