from flask import Flask, redirect, url_for
from config import Config
from models import db, login_manager
from flask_login import current_user

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import ALL models (VERY IMPORTANT for DB)
    from models.user import User
    from models.child import Child
    from models.parent import Parent
    from models.admin import Admin
    from models.saving_goal import SavingGoal
    from models.lesson import Lesson
    from models.lesson_activity import LessonActivity
    from models.gift import Gift

    # Import routes
    from routes.auth_routes import auth
    from routes.child_routes import child
    from routes.parent_routes import parent
    from routes.admin_routes import admin

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(child)
    app.register_blueprint(parent)
    app.register_blueprint(admin)

    # Role-based dashboard redirect
    @app.route('/dashboard')
    def dashboard():
        if current_user.is_authenticated:
            if current_user.role == 'child':
                return redirect(url_for('child.child_dashboard'))
            elif current_user.role == 'parent':
                return redirect(url_for('parent.parent_dashboard'))
            elif current_user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
        return redirect(url_for('auth.login'))

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # create all tables automatically
    app.run(debug=True)