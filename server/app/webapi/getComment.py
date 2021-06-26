from . import *

class GetComment(Resource):
    def get(self,record_id):
        r = RecordModel.find_by_id(record_id)
        r.view += 1
        db.session.commit()
        if len(r.comments) == 0:
            return jsonify(code=200,message='没有评论')
        commentInfo = {}
        for c in r.comments:
            commentInfo[c.id] = {
                'commit_time':str(c.commit_time),
                'content':c.content,
                'username': c.username,
                'stars': c.stars,
                'is_audio': c.is_audio,
                'audio_record': c.audio_record,
                'reply': [],
            }
            for reply in c.replys:
                commentInfo[c.id]['reply'].append({
                    'commit_time':str(reply.commit_time),
                    'content': reply.content,
                    'username': reply.username,
                    'receive_user': reply.receive_user,
                    'content': reply.content,
                })
        return jsonify(code=200, message='返回成功', commentInfo=commentInfo)