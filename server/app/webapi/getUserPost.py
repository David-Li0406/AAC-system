from . import *

class GetUserPost(Resource):
    @auth.login_required
    def get(self, page):
        retInfo = []
        r_page = RecordModel.find_by_public(page)
        for r in r_page.items:
            recordInfo = {
                'title': r.article_title,
                'content': r.article_content,
                'commit_time': str(r.commit_time),
                'username': r.user.username,
                'record_id': r.id,
                'view': r.view,
                'star': r.star,
                'comment': 0 if r.comments == None else len(r.comments)
            }
            retInfo.append(recordInfo)
        if page == 1:    
            return jsonify(code=200, message='返回成功', retInfo=retInfo, total=r_page.total)
        print(retInfo)
        return jsonify(code=200, message='返回成功', retInfo=retInfo)
        
            
