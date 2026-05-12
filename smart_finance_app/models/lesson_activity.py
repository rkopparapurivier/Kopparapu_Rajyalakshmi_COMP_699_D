from models import db

class LessonActivity(db.Model):
    __tablename__ = 'lesson_activity'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float)

    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))

    def update_score(self, score):
        self.score = score