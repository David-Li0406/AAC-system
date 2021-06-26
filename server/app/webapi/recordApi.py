from . import *

class RecordApi(Resource):
    @auth.login_required
    def get(self, record_id):
        record = RecordModel.find_by_id(record_id)
        if record is None:
            return jsonify(code=403, message='参数无效')
        r = RecordModel.find_by_id(record_id)
        if not r:
            return jsonify(code=403, message='作文id无效')
        origin_html = r.origin_html
        correction = {}
        recordInfo = {
            'title': r.article_title,
            'content': r.article_content,
            'time_cost': r.article_time_cost,
            'count': r.article_count,
            'public': r.public,
        }
        for word in r.wrongchars:
            correction[str(word.pos_id)] = {
                'origin_text_html': word.origin_text_html,
                'correct_text_html': word.correct_text_html,
                'context_html': word.context_html,
                'origin_text': word.origin_text,
                'correct_text': word.correct_text,
                'id': word.id,
                'collected': word.collected
            }
        article=[]
        for a in r.articles:
            article.append({
                'title': a.title,
                'content': a.content,
                'url': a.url,
            })
        correctionInfo = {
            'origin_html': origin_html,
            'correction': correction,
        }
        return jsonify(code=200, message='成功', recordInfo=recordInfo, correctionInfo= correctionInfo, recommand_article=article, public=r.public, record_id=r.id)