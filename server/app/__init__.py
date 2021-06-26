from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
# 导入配置文件
from config import DevelopConfig
from config import ProductConfig
 
# 初始化应用实例
app = Flask(__name__)
 
# 添加配置信息
app.config.from_object(DevelopConfig)

# 使应用支持跨域资源访问
CORS(app, supports_credentials=True)

# 创建api实例
api = Api(app)
 
# 初始化数据库
db = SQLAlchemy(app)

# 初始化auth认证
auth = HTTPTokenAuth(scheme="JWT")

# # 导入各资源类
from .webapi.loginApi import LoginApi
from .webapi.registerApi import RegisterApi
from .webapi.checkEmailApi import CheckEmailApi
from .webapi.checkUserApi import CheckUserApi
from .webapi.recordsApi import RecordsApi
from .webapi.searchWordApi import SearchWordApi
from .webapi.searchMaterialApi import SearchMaterialApi
from .webapi.imgOCRApi import ImgOCRApi
from .webapi.confirmApi import ConfirmApi
from .webapi.getHistoryApi import GetHistoryApi
from .webapi.deleteHistoryApi import DeleteHistoryApi
from .webapi.correctApi import CorrectApi
from .webapi.getNotebook import GetNotebook
from .webapi.addError import AddError
from .webapi.makePublic import MakePublic
from .webapi.getUserPost import GetUserPost
from .webapi.post import Post
from .webapi.postComment import PostComment
from .webapi.getComment import GetComment
from .webapi.postViewApi import StarPost, StarComment, PostReply
from .webapi.getUserInfo import GetUserInfo
from .webapi.getUserStat import GetUserStat
from .webapi.getUser import GetUser
from .webapi.deleteUser import DeleteUser
from .webapi.updateUser import UpdateUser
from .webapi.searchUser import SearchUser
from .webapi.recordApi import RecordApi

# # 绑定资源和URI
api.add_resource(LoginApi, '/api/login', endpoint='login')
api.add_resource(RegisterApi, '/api/register', endpoint='register')
api.add_resource(CheckEmailApi, '/api/checkEmail', endpoint='checkEmail')
api.add_resource(CheckUserApi, '/api/checkUser', endpoint='checkUser')
api.add_resource(RecordsApi, '/api/records', endpoint='records')
api.add_resource(SearchWordApi, '/api/searchWord', endpoint='searchWord')
api.add_resource(ConfirmApi,'/api/confirm',endpoint='confirm')
api.add_resource(SearchMaterialApi,'/api/searchMaterial', endpoint='searchMaterial')
api.add_resource(ImgOCRApi, '/api/imgOCR', endpoint='imgOCR')
api.add_resource(GetHistoryApi, '/api/getHistory', endpoint='getHistory')
api.add_resource(DeleteHistoryApi, '/api/deleteHistory', endpoint='deleteHistory')
api.add_resource(RecordApi, '/api/record/<int:record_id>', endpoint='record')
api.add_resource(GetNotebook, '/api/getNotebook', endpoint='getNotebook')
api.add_resource(AddError, '/api/addError', endpoint='addError')
api.add_resource(MakePublic, '/api/makePublic', endpoint='makePublic')
api.add_resource(GetUserPost, '/api/getUserPost/<int:page>', endpoint='getUserPost')
api.add_resource(Post, '/api/post/<int:record_id>', endpoint='post')
api.add_resource(PostComment, '/api/postComment', endpoint='postComment')
api.add_resource(GetComment, '/api/getComment/<int:record_id>', endpoint='getComment')
api.add_resource(StarPost, '/api/starPost', endpoint="starPost")
api.add_resource(StarComment, '/api/starComment', endpoint="starComment")
api.add_resource(PostReply, '/api/postReply', endpoint='postReply')
api.add_resource(GetUserInfo, '/api/getUserInfo/<string:username>', endpoint='getUserInfo')
api.add_resource(GetUserStat, '/api/getUserStat', endpoint='getUserStat')
api.add_resource(GetUser, '/api/getUser/<int:page>', endpoint='getUser')
api.add_resource(DeleteUser, '/api/deleteUser/<string:username>', endpoint='deleteUser')
api.add_resource(UpdateUser, '/api/updateUser/<string:username>', endpoint='updateUser')
api.add_resource(SearchUser, '/api/searchUser/<string:username>', endpoint='searchUser')
api.add_resource(CorrectApi, '/api/correct', endpoint='correct')