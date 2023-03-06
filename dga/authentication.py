from flask import Flask, render_template, url_for, request, redirect, flash, session, Blueprint
from functools import wraps
from .firebaseConfig import firebase

# for authentication
auth = firebase.auth()

authentication = Blueprint('authentication', __name__)

@authentication.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session.pop('_flashes', None) # clear flash messages 

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(auth.get_account_info(user['idToken']))
            session['email'] = email
            return redirect(url_for('rtdatabase.home'))
        except: # pylint: disable=W0702
            flash('Invalid username/password combination', 'error')
            return redirect(url_for('authentication.index'))

    return render_template('index.html')


@authentication.route('/logout')
def logout():
    auth.current_user = None
    session.pop('email', None)
    print('User logged out')
    return redirect(url_for('authentication.index'))


@authentication.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # we can use request.form.get() to avoid getting errors if the form field is empty
        # with this we will get None instead
        # email = request.form.get('email')
        # password = request.form.get('password')
        # confirm_password = request.form.get('cpassword')
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['cpassword']
        print(email, password, confirm_password)
        session.pop('_flashes', None) # clear flash messages 

        try:
            # Password must be looooooooong
            # You have to meet google's password complexity standards
            # if len(password) < 7:
            #     flash('Password must be at least 7 characters long', 'error')
            #     return redirect(url_for('registration'))

            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return redirect(url_for('authentication.registration'))

            auth.create_user_with_email_and_password(email, password)
            flash('Registration successful. You can login now.', 'msg')
            return redirect(url_for('authenication.index'))
        except: # pylint: disable=W0702
            flash('Email already exists', 'error')
            print('Email already exists', )
            return redirect(url_for('authentication.registration'))

    return render_template('registration.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            return redirect(url_for('authentication.index'))
        return f(*args, **kwargs)
    return decorated_function