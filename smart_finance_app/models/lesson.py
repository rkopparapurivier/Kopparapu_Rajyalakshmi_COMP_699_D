from models import db

class Lesson(db.Model):
    __tablename__ = 'lesson'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

    # Relationship
    activities = db.relationship('LessonActivity', backref='lesson', lazy=True)

    def update_content(self, new_content):
        self.content = new_content