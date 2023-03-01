from flask import Flask, render_template, url_for, request, redirect, flash, session
import pyrebase
import time

app = Flask(__name__)

firebaseConfig = {
    'apiKey': "AIzaSyAxk117Aj_aFukk_UBqwL3yp5f81FniZXI",
    'authDomain': "management-transformer.firebaseapp.com",
    'databaseURL': "https://management-transformer-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "management-transformer",
    'storageBucket': "management-transformer.appspot.com",
    'messagingSenderId': "26656610083",
    'appId': "1:26656610083:web:b0f3e1aa42ed6437781e96",
    'measurementId': "G-PX46R86W7N"
}

firebase = pyrebase.initialize_app(firebaseConfig)

# connect to database
auth = firebase.auth()

app.secret_key = 'abc123'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            auth.sign_in_with_email_and_password(email, password)
            session['email'] = email
            return redirect(url_for('home'))
        except: # pylint: disable=W0702
            flash('Invalid username/password combination', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
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
                return redirect(url_for('registration'))

            auth.create_user_with_email_and_password(email, password)
            flash('Registration successful. You can login now', 'msg')
            return redirect(url_for('login'))
        except: # pylint: disable=W0702
            flash('Email already exists', 'error')
            print('Email already exists', )
            return redirect(url_for('registration'))

    return render_template('registration.html')


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/records")
def records():
    return render_template("records.html")


if __name__ == "__main__":
    app.run(debug=True)
