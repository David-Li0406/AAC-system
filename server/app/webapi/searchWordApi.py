from . import *
import json
import requests

class SearchWordApi(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未接收到参数")
        query = req.get("query")

        url1 = 'https://aip.baidubce.com/oauth/2.0/token'
        para1 = {
            'grant_type': 'client_credentials',
            'client_id': app.config['BAIDU_APP_KEY'],
            'client_secret': app.config['BAIDU_SECRET_KEY'],
        }
        try:
            ret = requests.post(url = url1, data=para1).json()
            access_token = ret["access_token"]
        except:
            return jsonify(code=404, message="搜索失败")
        url2 = 'https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/chinese_search?access_token={}'.format(access_token)
        para2 = {
            "query": query
        }
        try:
            para2 = json.dumps(para2)
            headers = {
                'Content-Type': 'application/json'
            }
            ret = requests.post(url = url2, data=para2, headers = headers).json()
        except:
            return jsonify(code=404, message="搜索失败")
        print(ret)
        return jsonify(code = 200, message = "成功", wordInfo = ret)
        

