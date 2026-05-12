from models import db
from datetime import datetime

class Gift(db.Model):
    __tablename__ = 'gift'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    message = db.Column(db.String(200))
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    goal_id = db.Column(db.Integer, db.ForeignKey('saving_goal.id'))

    # -------------------------------
    # BUSINESS LOGIC METHODS
    # -------------------------------

    def apply_to_goal(self):
        if self.goal and self.amount:
            self.goal.saved_amount += self.amount