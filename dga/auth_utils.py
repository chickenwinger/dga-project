from functools import wraps
from flask import session, redirect, url_for

# decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('idToken'):
            return redirect(url_for('authentication.index'))
        return f(*args, **kwargs)
    return decorated_function