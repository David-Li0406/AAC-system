import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    #腾讯api密钥
    TENCENT_SECRET_KEY = 'bw1pMccLp2zf4C2cwzlHWUBcmgJfla7N'
    #腾讯api id
    TENCENT_SECRET_ID = 'AKIDNZUAZicFchW4KM9fvvf8uRkmX1EApDKB'
    #百度api密钥
    BAIDU_SECRET_KEY = 'Gtw646OumKcd5qvbD9f8dP9aq4epdCeK'
    #百度应用密钥
    BAIDU_APP_KEY = 'zYC6jHmkCM3rbvkeKCmkG7N3'
    # 调试模式
    DEBUG = False
    # 密钥
    SECRET_KEY = '1jjcd#23_dase1243'
    # 数据库连接
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    # 每次请求结束后自动追踪数据库变动
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 安全配置
    CSRF_ENABLED = True


# 开发环境下配置
class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:qwaszx@localhost:3306/aacdb?charset=utf8'


# 产品环境下配置
class ProductConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456789@202.112.194.244:3306/aacdb?charset=utf8'