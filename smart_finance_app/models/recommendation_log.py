from . import db
from datetime import datetime

class RecommendationLog(db.Model):
    __tablename__ = 'recommendation_log'

    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer)
    score = db.Column(db.Float)
    lesson_title = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)