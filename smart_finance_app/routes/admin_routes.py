from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from models import db
from models.lesson import Lesson
from models.user import User
from models.child import Child
from models.parent import Parent
from models.saving_goal import SavingGoal
from models.recommendation_log import RecommendationLog

admin = Blueprint('admin', __name__)


# ================= ADMIN ACCESS CHECK =================
def is_admin():
    return current_user.is_authenticated and current_user.role == "admin"


# 🔥 GLOBAL WEIGHTS (DEFAULT)
WEIGHTS = {
    "age": 0.3,
    "savings": 0.5,
    "behavior": 0.2
}


# ================= DASHBOARD =================
@admin.route('/admin/dashboard')
@login_required
def admin_dashboard():

    if not is_admin():
        flash("Access denied. Admins only.")
        return redirect('/')

    lessons = Lesson.query.all()

    # SYSTEM STATS
    total_users = User.query.count()
    total_children = Child.query.count()
    total_parents = Parent.query.count()
    total_goals = SavingGoal.query.count()
    total_lessons = Lesson.query.count()

    return render_template(
        'admin/admin_dashboard.html',
        lessons=lessons,
        total_users=total_users,
        total_children=total_children,
        total_parents=total_parents,
        total_goals=total_goals,
        total_lessons=total_lessons,
        weights=WEIGHTS   # 🔥 PASS TO UI
    )


# ================= UPDATE WEIGHTS (NEW) =================
@admin.route('/admin/update_weights', methods=['POST'])
@login_required
def update_weights():

    if not is_admin():
        flash("Access denied.")
        return redirect('/')

    try:
        WEIGHTS["age"] = float(request.form.get('age'))
        WEIGHTS["savings"] = float(request.form.get('savings'))
        WEIGHTS["behavior"] = float(request.form.get('behavior'))

        flash("Weights updated successfully!")

    except:
        flash("Invalid values entered.")

    return redirect('/admin/dashboard')


# ================= ADD LESSON =================
@admin.route('/lesson/add', methods=['POST'])
@login_required
def add_lesson():

    if not is_admin():
        flash("Access denied.")
        return redirect('/')

    title = request.form.get('title')
    content = request.form.get('content')

    if not title or not content:
        flash("Please fill all fields.")
        return redirect('/admin/dashboard')

    lesson = Lesson(
        title=title,
        content=content
    )

    db.session.add(lesson)
    db.session.commit()

    flash("Lesson added successfully!")
    return redirect('/admin/dashboard')


# ================= EDIT LESSON =================
@admin.route('/lesson/edit/<int:id>', methods=['POST'])
@login_required
def edit_lesson(id):

    if not is_admin():
        flash("Access denied.")
        return redirect('/')

    lesson = Lesson.query.get(id)

    if not lesson:
        flash("Lesson not found.")
        return redirect('/admin/dashboard')

    lesson.content = request.form.get('content')

    db.session.commit()

    flash("Lesson updated successfully!")
    return redirect('/admin/dashboard')


# ================= MANAGE PAGE =================
@admin.route('/manage_lessons')
@login_required
def manage_lessons():

    if not is_admin():
        flash("Access denied.")
        return redirect('/')

    lessons = Lesson.query.all()
    return render_template('admin/manage_lessons.html', lessons=lessons)


# ================= VIEW LOGS =================
@admin.route('/admin/logs')
@login_required
def view_logs():

    if not is_admin():
        flash("Access denied.")
        return redirect('/')

    logs = RecommendationLog.query.order_by(
        RecommendationLog.timestamp.desc()
    ).all()

    return render_template('admin/logs.html', logs=logs)