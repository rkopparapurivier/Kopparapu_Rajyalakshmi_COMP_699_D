from app import app
from models import db
from models.user import User
from models.admin import Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    existing = User.query.filter_by(email="admin@kopraji.com").first()

    if not existing:
        admin_user = User(
            name="KopRaji Admin",
            email="admin@kopraji.com",
            password=generate_password_hash("KopRaji@2026Secure"),
            role="admin"
        )

        db.session.add(admin_user)
        db.session.commit()

        admin = Admin(user_id=admin_user.id)
        db.session.add(admin)
        db.session.commit()

        print("✅ Admin created successfully!")
    else:
        print("⚠️ Admin already exists!")