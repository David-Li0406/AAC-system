from . import *
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models
import json

class SearchMaterialApi(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未接收到参数")
        SrcText = req.get('material')
        TargetText = []
        with open('data/material_topic.txt', 'r', encoding = 'utf8')as f:
            for line in f:
                TargetText.append(line)
        try: 
            cred = credential.Credential(app.config['TENCENT_SECRET_ID'], app.config['TENCENT_SECRET_KEY']) 
            httpProfile = HttpProfile()
            httpProfile.endpoint = "nlp.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = nlp_client.NlpClient(cred, 'ap-guangzhou', clientProfile) 

            req = models.TextSimilarityRequest()
            params = {
                "SrcText": SrcText,
                "TargetText": TargetText
            }
            req.from_json_string(json.dumps(params))

            resp = client.TextSimilarity(req)
            resp_dic =json.loads(resp.to_json_string())
            top = sorted(resp_dic['Similarity'], key = lambda i:i['Score'], reverse=True)[0]
            data = MaterialModel.find_by_topic(top['Text'].strip())[:5]
            materialInfo = [{
                'title' : item.title,
                'content' : item.content,
                'url' : item.url,
            } for item in data]
            return jsonify(code=200, message="搜索成功", materialInfo=materialInfo)

        except TencentCloudSDKException as err: 
            print(err)
            return jsonify(code=404, message="搜索失败")