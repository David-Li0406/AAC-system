from . import *
import requests

class ImgOCRApi(Resource):
    @auth.login_required
    def post(self):
        req = request.json
        if req is None:
            return jsonify(code=403, message="未接收到参数")
        img = req.get("img_base64")

        url1 = 'https://aip.baidubce.com/oauth/2.0/token'
        para1 = {
            'grant_type': 'client_credentials',
            'client_id': app.config['BAIDU_APP_KEY'],
            'client_secret': app.config['BAIDU_SECRET_KEY'],
        }
        try:
            ret = requests.post(url = url1, data=para1).json()
            access_token = ret["access_token"]
        except Exception as e:
            print(e)
            return jsonify(code=404, message="识别失败")
        import json
        url2 = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}'.format(access_token)
        para2 = {
            "image": img,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            ret = requests.post(url = url2, data=para2, headers = headers).json()
        except Exception as e:
            print(e)
            return jsonify(code=404, message="识别失败")

        title = ret['words_result'][0]['words']
        content = ''
        for i in range(1, len(ret['words_result'])):
            content += ret['words_result'][i]['words']
        OCR_res = {
            'title': title,
            'content': content
        }
        return jsonify(code=200, message="识别成功", OCR_res=OCR_res)
