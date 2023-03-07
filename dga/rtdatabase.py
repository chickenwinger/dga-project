from flask import Flask, render_template, url_for, request, redirect, flash, session, Blueprint
from dga import db, auth
import time
from .firebaseConfig import firebase
from .auth_utils import login_required


rtdatabase = Blueprint('rtdatabase', __name__)

@rtdatabase.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        user = auth.get_account_info(session['idToken'])['users'][0]
                
        if request.form['action'] == 'record':
            # print(user["localId"])
            # print(auth.current_user)
            add_record(user)
            
            flash('Record added successfully', 'msg')
            return redirect(url_for('rtdatabase.home'))
        
        

    return render_template("home.html")


@rtdatabase.route("/records")
@login_required
def records():
    return render_template("records.html")


def add_record(user):
    record = request.form.get('rname')
    hydrogen = request.form.get('hydrogenconc')
    methane = request.form.get('methaneconc')
    acetylene = request.form.get('acetyleneconc')
    ethylene = request.form.get('ethyleneconc')
    ethane = request.form.get('ethaneconc')
    cmonoxide = request.form.get('cmonoxideconc')
    cdioxide = request.form.get('cdioxideconc')
    total = request.form.get('totalcombustibles')
        
    data = {
        "timestamp": time.time(), # firebase.database.ServerValue.TIMESTAMP,
        "hydrogen": hydrogen,
        "methane": methane,
        "acetylene": acetylene,
        "ethylene": ethylene,
        "ethane": ethane,
        "cmonoxide": cmonoxide,
        "cdioxide": cdioxide,
        "total_combustibles": total
    }
    
    ref = db.child("records").child(user["localId"])
    
    if ref.get().val() is None:
        db.child("records").child(user["localId"]).set({record: data})
        return redirect(url_for('rtdatabase.home'))
    
    if ref.child(record).get().val() is not None:
        flash('Record name already exists', 'error')
        return redirect(url_for('rtdatabase.home'))
    
    ref.child(record).set(data)
    return redirect(url_for('rtdatabase.home'))