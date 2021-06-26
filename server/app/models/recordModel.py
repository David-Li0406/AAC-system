from . import *
from datetime import datetime

record_article = db.Table('record_article',
					 db.Column('record_id', db.Integer, db.ForeignKey('records.id'), primary_key=True),
					 db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True)
					 )


class RecordModel(db.Model):

    # 对应表格records
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    # 因为可能会用时间查询，所以建立一个索引
    commit_time = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    article_title = db.Column(db.String(100), nullable=False, default='')
    article_content = db.Column(db.Text, nullable=False, default='')
    article_count = db.Column(db.Integer, default=0)
    article_time_cost = db.Column(db.String(20), default='00:00:00')
    origin_html = db.Column(db.String(1500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    state = db.Column(db.Integer, default=1)
    public = db.Column(db.Boolean, default=False, index=True)
    view = db.Column(db.Integer, default=0, nullable=False)
    star = db.Column(db.Integer, default=0, nullable=False)

    wrongchars = db.relationship('CorrectionModel', backref='record')
    articles = db.relationship('ArticleModel', secondary=record_article, backref=db.backref('records'))
    comments = db.relationship('CommentModel', backref='record')
    replys = db.relationship('ReplyModel', backref='record')

    def __repr__(self):
        return '<Record %s>' % self.id

    def __init__(self, article_title, article_content, article_count, article_time_cost, origin_html, user_id):
        self.article_title = article_title
        self.article_content = article_content
        self.article_count = article_count
        self.article_time_cost = article_time_cost
        self.origin_html = origin_html
        self.user_id = user_id

    def add_record(self):
        db.session.add(self)
        db.session.commit()

    def delete_record(self):
        for w in self.wrongchars:
            w.delete_wrongchar_record()
        for c in self.comments:
            c.delete_comment()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_public(cls, page, per_page=5):
        return cls.query.filter_by(public=True).paginate(page,per_page=per_page)

    # 找到当前用户时间范围记录
    @classmethod
    def find_by_time(cls, start_time, end_time):
        return db.session.query(cls).filter(cls.user_id==g.user.id).filter(cls.commit_time.between(start_time, end_time)).all()