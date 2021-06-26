from flask_restful import Resource
from app import auth
from app import db
from .. import app

from ..models.userModel import UserModel
from ..models.recordModel import RecordModel
from ..models.correctionModel import CorrectionModel
from ..models.verificationCodeModel import VerificationCodeModel
from ..models.materialModel import MaterialModel
from ..models.articleModel import ArticleModel
from ..models.commentModel import CommentModel
from ..models.replyModel import ReplyModel

from flask import json, jsonify, request, abort, g

@auth.verify_token
def verify_token(token):
    user = UserModel.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

