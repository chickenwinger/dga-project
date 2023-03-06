from flask import Flask, render_template, url_for, request, redirect, flash, session, Blueprint
from .authentication import login_required
from .firebaseConfig import firebase


# for firebase realtime database
db = firebase.database()
# for firebase storage but we will not use it in this app
# storage = firebase.storage()

rtdatabase = Blueprint('rtdatabase', __name__)

@rtdatabase.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html")


@rtdatabase.route("/records")
@login_required
def records():
    return render_template("records.html")