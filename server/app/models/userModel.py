#!/usr/bin/env python
#-*- coding:utf8 -*-
# 用户数据库模型


from . import *
from datetime import datetime


class UserModel(db.Model, UserMixin):
    # 对应表格：users
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    nickname = db.Column(db.String(64), default='')
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    register_time = db.Column(db.DateTime, default=datetime.now)
    user_type = db.Column(db.String(16), default='user')
    total_time_cost = db.Column(db.Integer, default=0)
    total_count = db.Column(db.Integer, default=0)
    total_mistake = db.Column(db.Integer, default=0)
    total_record = db.Column(db.Integer, default=0)


    records = db.relationship('RecordModel', backref='user')
    comments = db.relationship('CommentModel', backref='user')
    replys = db.relationship('ReplyModel', backref='user')

    def __init__(self, username, email, nickname):
        self.username = username
        self.email = email
        self.nickname = nickname

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 密码设置
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码验证
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    # 生成token
    def generate_auth_token(self, expiration=3600):
        s = Serializer(app.config['SECRET_KEY'], expiration)
        return s.dumps({'id':self.id}).decode("ascii")

    # 解析token，确认登陆用户的身份
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = UserModel.query.get(data['id'])
        return user

    # 信息打包成json
    def to_json(self):
        return jsonify(
            code=200,
            message="成功",
            id=self.id,
            username=self.username,
            email=self.email
        )

    # 通过用户名获取用户
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # 通过邮箱获取用户
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all_user(cls, page, per_page=1):
        return cls.query.filter_by(user_type='user').paginate(page,per_page=per_page)

    # 新增用户
    def add_user(self):
        db.session.add(self)
        db.session.commit()

    # 删除用户
    def delete_user(self):
        for r in self.records:
            r.delete_record()
        for c in self.comments:
            c.delete_comment()
        for reply in self.replys:
            reply.delete_reply()
        db.session.delete(self)
        db.session.commit()

    #设为管理员
    def set_administrator(self):
        self.user_type = 'administrator'
        db.session.commit()
        

