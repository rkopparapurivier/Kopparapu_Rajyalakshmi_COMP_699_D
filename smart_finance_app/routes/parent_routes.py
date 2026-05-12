from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from models import db
from models.parent import Parent
from models.child import Child
from models.saving_goal import SavingGoal
from models.gift import Gift

parent = Blueprint('parent', __name__)


# ================= DASHBOARD =================
@parent.route('/parent/dashboard')
@login_required
def parent_dashboard():
    parent_obj = Parent.query.filter_by(user_id=current_user.id).first()

    if not parent_obj:
        flash("Parent profile not found.")
        return redirect('/')

    return render_template(
        'parent/parent_dashboard.html',
        children=parent_obj.children
    )


# ================= LINK CHILD USING CODE =================
@parent.route('/link_child', methods=['POST'])
@login_required
def link_child():
    parent_obj = Parent.query.filter_by(user_id=current_user.id).first()

    code = request.form.get('child_code')

    if not code:
        flash("Please enter child code.")
        return redirect('/parent/dashboard')

    child = Child.query.filter_by(unique_code=code).first()

    if not child:
        flash("Invalid child code.")
        return redirect('/parent/dashboard')

    child.parent_id = parent_obj.id
    db.session.commit()

    flash("Child linked successfully!")
    return redirect('/parent/dashboard')


# ================= SET REMINDER =================
@parent.route('/set_reminder/<int:child_id>', methods=['POST'])
@login_required
def set_reminder(child_id):
    child = Child.query.get(child_id)

    if not child:
        flash("Child not found.")
        return redirect('/parent/dashboard')

    text = request.form.get('reminder_text')
    amount = request.form.get('reminder_amount')

    if not text or not amount:
        flash("Please enter reminder details.")
        return redirect('/parent/dashboard')

    try:
        amount = float(amount)
    except:
        flash("Invalid amount.")
        return redirect('/parent/dashboard')

    child.reminder_text = text
    child.reminder_amount = amount

    db.session.commit()

    flash("Reminder set successfully!")
    return redirect('/parent/dashboard')


# ================= CHILD DETAILS PAGE (NEW) =================
@parent.route('/parent/child/<int:id>')
@login_required
def child_details(id):
    child = Child.query.get(id)

    if not child:
        flash("Child not found.")
        return redirect('/parent/dashboard')

    # Collect all gifts for this child
    all_gifts = []
    for goal in child.goals:
        if hasattr(goal, 'gifts'):
            all_gifts.extend(goal.gifts)

    return render_template(
        'parent/child_details.html',
        child=child,
        gifts=all_gifts
    )


# ================= OPEN GIFT PAGE =================
@parent.route('/gift/<int:goal_id>')
@login_required
def gift_page(goal_id):
    goal = SavingGoal.query.get(goal_id)

    if not goal:
        flash("Goal not found.")
        return redirect('/parent/dashboard')

    return render_template('parent/send_gift.html', goal=goal)


# ================= SEND GIFT =================
@parent.route('/send_gift/<int:goal_id>', methods=['POST'])
@login_required
def send_gift(goal_id):
    amount = request.form.get('amount')
    message = request.form.get('message')

    try:
        amount = float(amount)
    except:
        flash("Invalid amount.")
        return redirect('/parent/dashboard')

    gift = Gift(amount=amount, message=message, goal_id=goal_id)
    db.session.add(gift)

    goal = SavingGoal.query.get(goal_id)

    if goal:
        goal.saved_amount += amount

    db.session.commit()

    flash("Gift sent successfully!")
    return redirect('/parent/dashboard')