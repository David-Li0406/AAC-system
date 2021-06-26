from . import *
from datetime import datetime
from sqlalchemy.dialects.mysql import LONGTEXT

class CommentModel(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    commit_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False, default='')
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"), nullable = False)
    username = db.Column(db.String(64), db.ForeignKey('users.username'),nullable = False, index=True)
    stars = db.Column(db.Integer, nullable=False, default=0)
    audio_record = db.Column(LONGTEXT, default='')
    is_audio = db.Column(db.Boolean, default=False)

    replys = db.relationship('ReplyModel', backref='comment')

    def __init__(self, content, username, record_id, is_audio = False, audio_record=''):
        self.content = content
        self.username = username
        self.record_id = record_id
        self.is_audio = is_audio
        self.audio_record = audio_record

    def add_comment(self):
        db.session.add(self)
        db.session.commit()

    def add_star(self):
        self.stars += 1
        db.session.commit()

    def delete_comment(self):
        for r in self.replys:
            r.delete_reply()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()