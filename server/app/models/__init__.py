from werkzeug.security import generate_password_hash, check_password_hash
# 生成令牌函数
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask_login import UserMixin
from .. import db, app
from flask import json, jsonify, request, abort, g

from .userModel import UserModel
from .recordModel import RecordModel
from .correctionModel import CorrectionModel
from .verificationCodeModel import VerificationCodeModel
from .materialModel import MaterialModel
from .articleModel import ArticleModel
from .commentModel import CommentModel
from .replyModel import ReplyModel