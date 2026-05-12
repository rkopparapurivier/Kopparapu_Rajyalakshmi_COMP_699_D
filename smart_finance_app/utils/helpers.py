from datetime import datetime


# -------------------------------
# VALIDATION HELPERS
# -------------------------------

def validate_positive_number(value):
    try:
        value = float(value)
        return value > 0
    except:
        return False


def validate_text(text):
    return text is not None and text.strip() != ""


# -------------------------------
# CALCULATION HELPERS
# -------------------------------

def calculate_progress(saved, target):
    if target == 0:
        return 0
    return round((saved / target) * 100, 2)


# -------------------------------
# DATE FORMATTING
# -------------------------------

def format_date(date_obj):
    if not date_obj:
        return ""
    return date_obj.strftime("%d-%m-%Y")


# -------------------------------
# USER ROLE CHECK
# -------------------------------

def is_child(user):
    return user.role == 'child'


def is_parent(user):
    return user.role == 'parent'


def is_admin(user):
    return user.role == 'admin'


# -------------------------------
# SAFE DATA FETCH
# -------------------------------

def safe_float(value):
    try:
        return float(value)
    except:
        return 0


# -------------------------------
# MESSAGE FORMAT
# -------------------------------

def success_message(msg):
    return f"✔ {msg}"


def error_message(msg):
    return f"✖ {msg}"