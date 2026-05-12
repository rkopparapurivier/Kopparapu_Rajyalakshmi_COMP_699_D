from models import db

class SavingGoal(db.Model):
    __tablename__ = 'saving_goal'

    id = db.Column(db.Integer, primary_key=True)
    goal_name = db.Column(db.String(100), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    saved_amount = db.Column(db.Float, default=0)

    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))

    # Relationship with Gift
    gifts = db.relationship('Gift', backref='goal', lazy=True)

    # -------------------------------
    # BUSINESS LOGIC METHODS
    # -------------------------------

    def add_amount(self, amount):
        if amount > 0:
            self.saved_amount += amount

    def edit_goal(self, new_name):
        if new_name and new_name.strip() != "":
            self.goal_name = new_name

    def get_progress(self):
        if self.target_amount == 0:
            return 0
        return round((self.saved_amount / self.target_amount) * 100, 2)