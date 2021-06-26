from . import *

class CorrectionModel(db.Model):

    __tablename__ = "wrongchars"
    id = db.Column(db.Integer, primary_key = True)
    origin_text_html = db.Column(db.String(300), nullable = False)
    correct_text_html = db.Column(db.String(300), nullable = False)
    pos_id = db.Column(db.Integer, nullable = False)
    context_html = db.Column(db.String(300), nullable = False)
    origin_text = db.Column(db.String(10), nullable = False)
    correct_text = db.Column(db.String(10), nullable = False)
    collected = db.Column(db.Boolean,index=True, default=False)
    record_id = db.Column(db.Integer, db.ForeignKey("records.id"), nullable = False)

    def __repr__(self):
        return '<WrongChar: %s>' % self.id

    def __init__(self, origin_text_html, correct_text_html, pos_id, context_html, origin_text, correct_text, record_id):
        self.origin_text_html = origin_text_html
        self.correct_text_html = correct_text_html
        self.pos_id = pos_id
        self.context_html = context_html
        self.origin_text = origin_text
        self.correct_text = correct_text
        self.record_id = record_id

    def add_wrongchar_record(self):
        db.session.add(self)
        db.session.commit()

    def delete_wrongchar_record(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_record_id(cls, record_id):
        return cls.query.filter_by(record_id=record_id).first()

    @classmethod
    def find_by_collected(cls, record_id):
        return cls.query.filter_by(record_id=record_id,collected=True).all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
