from . import *
from datetime import datetime

class ReplyModel(db.Model):

    __tablename__ = 'reply'

    id = db.Column(db.Integer, primary_key=True)
    commit_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False, default='')
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"), nullable = False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"), nullable = False)
    # 加一个外键为了算用户的总回复数量
    username = db.Column(db.String(64), db.ForeignKey('users.username'), index=True)
    receive_user = db.Column(db.String(64), index=True)
    content = db.Column(db.Text, nullable=False, default='')

    def __init__(self, record_id, comment_id, reply_user, receive_user, content):
        self.record_id = record_id
        self.comment_id = comment_id
        self.username = reply_user
        self.receive_user = receive_user
        self.content = content

    def add_reply(self):
        db.session.add(self)
        db.session.commit()

    def delete_reply(self):
        db.session.delete(self)
        db.session.commit()

    #用来在post页面根据每个comment取reply
    def find_by_comment_id(cls, comment_id):
        return cls.query.filter_by(comment_id=comment_id)