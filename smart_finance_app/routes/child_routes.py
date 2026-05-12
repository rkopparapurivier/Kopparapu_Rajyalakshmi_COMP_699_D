from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from models import db
from models.child import Child
from models.saving_goal import SavingGoal
from models.lesson import Lesson
from models.lesson_activity import LessonActivity
from models.recommendation_log import RecommendationLog
from ml_engine.engine import MLEngine

# 🔥 IMPORT ADMIN WEIGHTS
from routes.admin_routes import WEIGHTS

child = Blueprint('child', __name__)


# ================= DASHBOARD =================
@child.route('/child/dashboard')
@login_required
def child_dashboard():
    child_obj = Child.query.filter_by(user_id=current_user.id).first()

    if not child_obj:
        flash("Child profile not found.")
        return redirect('/')

    # Collect all gifts
    all_gifts = []
    for goal in child_obj.goals:
        if hasattr(goal, 'gifts'):
            all_gifts.extend(goal.gifts)

    return render_template(
        'child/child_dashboard.html',
        goals=child_obj.goals,
        gifts=all_gifts,
        child=child_obj
    )


# ================= ADD GOAL =================
@child.route('/goal/add', methods=['POST'])
@login_required
def add_goal():
    child_obj = Child.query.filter_by(user_id=current_user.id).first()

    name = request.form.get('name')
    amount = request.form.get('amount')

    if not name or not amount:
        flash("Please enter all fields.")
        return redirect('/child/dashboard')

    try:
        amount = float(amount)
    except:
        flash("Invalid amount entered.")
        return redirect('/child/dashboard')

    goal = SavingGoal(
        goal_name=name,
        target_amount=amount,
        child_id=child_obj.id
    )

    db.session.add(goal)
    db.session.commit()

    flash("Goal added successfully!")
    return redirect('/child/dashboard')


# ================= ADD AMOUNT =================
@child.route('/goal/add_amount/<int:id>', methods=['POST'])
@login_required
def add_amount(id):
    goal = SavingGoal.query.get(id)

    if not goal:
        flash("Goal not found.")
        return redirect('/child/dashboard')

    amount = request.form.get('amount')

    try:
        amount = float(amount)
    except:
        flash("Invalid amount.")
        return redirect('/child/dashboard')

    goal.add_amount(amount)
    db.session.commit()

    flash("Savings updated successfully!")
    return redirect('/child/dashboard')


# ================= LESSON =================
@child.route('/lesson')
@login_required
def lesson():
    child_obj = Child.query.filter_by(user_id=current_user.id).first()
    lessons = Lesson.query.all()

    if not lessons:
        flash("No lessons available yet.")
        return redirect('/child/dashboard')

    # 🔥 USE UPDATED ENGINE WITH WEIGHTS
    engine = MLEngine(WEIGHTS)

    score = engine.apply_rule_model(
        child_obj.age,
        child_obj.calculate_total_savings(),
        child_obj.behavior_score
    )

    selected = engine.select_personalized_lesson(score, lessons)

    # 🔥 SAVE LOG
    log = RecommendationLog(
        child_id=child_obj.id,
        score=score,
        lesson_title=selected.title
    )

    db.session.add(log)
    db.session.commit()

    return render_template('child/lesson.html', lesson=selected)


# ================= ACTIVITY =================
@child.route('/activity/<int:lesson_id>', methods=['POST'])
@login_required
def complete_activity(lesson_id):
    child_obj = Child.query.filter_by(user_id=current_user.id).first()

    score = request.form.get('score')

    try:
        score = float(score)

        # 🔥 VALIDATION (NEW)
        if score < 0 or score > 10:
            flash("Score must be between 0 and 10")
            return redirect('/child/dashboard')

    except:
        flash("Invalid score entered.")
        return redirect('/child/dashboard')

    activity = LessonActivity(
        score=score,
        child_id=child_obj.id,
        lesson_id=lesson_id
    )

    child_obj.update_learning_score(score)

    db.session.add(activity)
    db.session.commit()

    flash("Activity completed successfully!")
    return redirect('/child/dashboard')


# ================= EDIT GOAL =================
@child.route('/goal/edit/<int:id>', methods=['POST'])
@login_required
def edit_goal(id):
    goal = SavingGoal.query.get(id)

    if not goal:
        flash("Goal not found.")
        return redirect('/child/dashboard')

    new_name = request.form.get('name')

    if not new_name or new_name.strip() == "":
        flash("Goal name cannot be empty.")
        return redirect('/child/dashboard')

    goal.goal_name = new_name
    db.session.commit()

    flash("Goal updated successfully!")
    return redirect('/child/dashboard')


# ================= PROGRESS PAGE =================
@child.route('/child/progress')
@login_required
def child_progress():
    child_obj = Child.query.filter_by(user_id=current_user.id).first()

    if not child_obj:
        flash("Child profile not found.")
        return redirect('/child/dashboard')

    return render_template(
        'child/progress.html',
        child=child_obj
    )