from flask import render_template, session
from functools import wraps


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            # Display message instead of redirecting
            return render_template('error.html', message="Dostęp do strony wymaga uprawnień admina")
        return f(*args, **kwargs)

    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            # Display message instead of redirecting
            return render_template('error.html', message="Dostęp do strony wymaga zalogowania")
        return f(*args, **kwargs)

    return decorated_function
