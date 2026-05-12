from models import db
import random

class Child(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    learning_score = db.Column(db.Float, default=0)
    behavior_score = db.Column(db.Float, default=0)

    # 🔥 Unique Code for Parent Linking
    unique_code = db.Column(db.String(6), unique=True)

    # 🔥 Saving Reminder Fields
    reminder_text = db.Column(db.String(200))
    reminder_amount = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))

    # Relationships
    goals = db.relationship('SavingGoal', backref='child', lazy=True)
    activities = db.relationship('LessonActivity', backref='child', lazy=True)

    # -------------------------------
    # AUTO GENERATE UNIQUE CODE
    # -------------------------------
    def generate_unique_code(self):
        return str(random.randint(100000, 999999))

    # -------------------------------
    # BUSINESS LOGIC METHODS
    # -------------------------------
    def calculate_total_savings(self):
        return sum(goal.saved_amount for goal in self.goals)

    def update_learning_score(self, score):
        if score > 0:
            self.learning_score += score

    # -------------------------------
    # LEARNING BADGE LOGIC
    # -------------------------------
    def get_learning_badge(self):
        if self.learning_score < 40:
            return "Bronze"
        elif self.learning_score < 70:
            return "Silver"
        else:
            return "Gold"

    # -------------------------------
    # GOAL PROGRESS METHODS
    # -------------------------------
    def get_completed_goals(self):
        return sum(1 for goal in self.goals if goal.saved_amount >= goal.target_amount)

    def get_total_goals(self):
        return len(self.goals)

    # -------------------------------
    # LESSON PROGRESS METHODS (NEW)
    # -------------------------------
    def get_total_activities(self):
        return len(self.activities)

    def get_average_score(self):
        if len(self.activities) == 0:
            return 0
        total = sum(activity.score for activity in self.activities)
        return round(total / len(self.activities), 2)