from flask import Blueprint, render_template, request, redirect, flash
from models import db
from models.user import User
from models.child import Child
from models.parent import Parent

from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

import random

auth = Blueprint('auth', __name__)


# ================= LOGIN =================
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/dashboard')
        else:
            flash("Invalid email or password")

    return render_template('login.html')


# ================= REGISTER =================
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        role = request.form.get('role')

        # 🔒 SECURITY FIX: Prevent admin registration
        if role == 'admin':
            flash("Admin registration is not allowed.")
            return redirect('/register')

        # Check duplicate email
        if User.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect('/register')

        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        # -------------------------------
        # CREATE ROLE RECORD
        # -------------------------------
        if role == 'child':

            # Generate unique 6-digit code
            def generate_code():
                while True:
                    code = str(random.randint(100000, 999999))
                    if not Child.query.filter_by(unique_code=code).first():
                        return code

            child = Child(
                user_id=user.id,
                age=10,
                unique_code=generate_code()
            )

            db.session.add(child)

        elif role == 'parent':
            db.session.add(Parent(user_id=user.id))

        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect('/')

    return render_template('register.html')


# ================= LOGOUT =================
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')