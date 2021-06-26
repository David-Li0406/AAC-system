from . import *
import requests
import re
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
import json
import time


def convStr2Sec(s):
    h,m,s = s.split(':')
    return (int(h[0])*10+int(h[1]))*3600+(int(m[0])*10+int(m[1]))*60+int(s[0])*10+int(s[1])


def correct_byWenXin(essay):
    
    headers = {
        "Accept":"pplication/json, text/plain, */*", 
        "Accept-Encoding":"gzip, deflate", 
        "Accept-Language":"zh-CN, zh;q = 0.9", 
        "Content-Type":"application/x-www-form-urlencoded;charset = UTF-8"
    }
    
    data_write = {
        "content":essay
    }
    data_write = json.dumps(data_write)
    url_write = "http://202.112.194.61:8091/api/gec/write"
    r = requests.post(url=url_write, headers=headers, data=data_write)
    data_check = {
        "id":re.search('\d+', r.text).group(0)
    }
    data_check = json.dumps(data_check)
    url_check = "http://202.112.194.61:8091/api/gec/check"
    r = requests.post(url=url_check, headers=headers, data=data_check)
    print(r.text)
    result = r.json()
    return result["essay"]["problem_detail"], result["essay"]["origin_html"]

class RecordsApi(Resource):
    @auth.login_required
    def post(self):

        req = request.json
        if req is None:
            return jsonify(code=403, message="未接收到参数")

        articleTitle = req.get("title")
        articleContent = req.get("content")
        articleCount = req.get("count")
        articleTimeCost = req.get("time_cost")
        paragragh = "|"
        problem_detail, origin_html = correct_byWenXin(paragragh.join(articleContent.split('\n')))
        r = RecordModel(articleTitle, articleContent, articleCount, articleTimeCost, origin_html, g.user.id)
        r.add_record()
        for word in problem_detail:
            origin_text = word['origin_text']
            correct_text = word['correct_text']
            origin_text_html = "<span class='origin-text-class' id="+str(word['id'])+">"+word['origin_text']+"</span>"
            correct_text_html = word['correct_text_html']
            pos_id = word['id']
            context_html = word['token_str']
            problem_detail_data = CorrectionModel(origin_text_html, correct_text_html, pos_id, context_html, origin_text, correct_text, r.id)
            problem_detail_data.add_wrongchar_record()

        
        TargetText = []
        with open('data/article_topic.txt', 'r', encoding = 'utf8')as f:
            for line in f:
                TargetText.append(line)
        try: 
            cred = credential.Credential(app.config['TENCENT_SECRET_ID'], app.config['TENCENT_SECRET_KEY']) 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "nlp.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = nlp_client.NlpClient(cred, 'ap-guangzhou', clientProfile) 

            #先算前100个
            req = models.TextSimilarityRequest()
            params1 = {
                "SrcText": articleTitle,
                "TargetText": TargetText[:100]
            }
            req.from_json_string(json.dumps(params1))
            resp = client.TextSimilarity(req)
            resp_dic =json.loads(resp.to_json_string())

            #再算后边的
            time.sleep(2)
            req = models.TextSimilarityRequest()
            params2 = {
                "SrcText": articleTitle,
                "TargetText": TargetText[100:]
            }
            req.from_json_string(json.dumps(params2))
            resp = client.TextSimilarity(req)
            resp_dic['Similarity'] += json.loads(resp.to_json_string())['Similarity']

            top = sorted(resp_dic['Similarity'], key = lambda i:i['Score'], reverse=True)[0]
            data = ArticleModel.find_by_topic(top['Text'].strip())[:20]
            r.articles += data
            db.session.add(r)

            u=g.user
            u.total_count += articleCount
            u.total_record += 1
            u.total_time_cost += convStr2Sec(articleTimeCost)
            u.total_mistake += len(problem_detail)
            db.session.commit()
            
        except Exception as err: 
            print(err)

        return jsonify(code = 200, message = "成功", recordId = r.id)