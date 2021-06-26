from . import *

class ArticleModel(db.Model):

    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False, default='', index=True)
    title = db.Column(db.String(100), nullable=False, default='')
    content = db.Column(db.Text, nullable=False, default='')
    url = db.Column(db.String(100), nullable=False, default='')

    def __repr__(self):
        return '<Article %s>' % self.id

    def __init__(self, topic, title, content, url):
        self.topic = topic
        self.title = title
        self.content = content
        self.url = url
    
    def add_record(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_topic(cls, topic):
        return cls.query.filter_by(topic = topic).all()