from flask import Flask, render_template, url_for, request, redirect, flash, session, Blueprint
from dga import db, auth
from collections import OrderedDict
import time
from .firebaseConfig import firebase
from .auth_utils import login_required
from .dga_utils import dt1, dt4, dt5, pentagon1, pentagon2


rtdatabase = Blueprint('rtdatabase', __name__)

@rtdatabase.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        user = auth.get_account_info(session['idToken'])['users'][0]
                
        if request.form['action'] == 'record':
            print(request.form)
            if add_record(user):
                flash('Record name already exists', 'error')
                return render_template("home.html")
            else:
                flash('Record added successfully', 'msg')
                return redirect(url_for('rtdatabase.home'))
            
            # print(get_last_record())
        else:
            ordered_dict = get_last_record()
            record_query = next(iter(ordered_dict.values()))
            hydrogen = int(record_query['hydrogen'])
            methane = int(record_query['methane'])
            acetylene = int(record_query['acetylene'])
            ethylene = int(record_query['ethylene'])
            ethane = int(record_query['ethane'])
            cmonoxide = int(record_query['cmonoxide'])
            cdioxide = int(record_query['cdioxide'])
            
            dt1(ethylene, methane, acetylene)
            dt4(methane, hydrogen, ethane)
            dt5(ethylene, methane, ethane)
            pentagon1(ethane, hydrogen, acetylene, ethylene, methane)
            pentagon2(ethane, hydrogen, acetylene, ethylene, methane)
            
            img = None
            if request.form['action'] == 'triangle1':
                img = 1
            if request.form['action'] == 'triangle4':
                img = 2
            if request.form['action'] == 'triangle5':
                img = 3
            if request.form['action'] == 'pentagon1':
                img = 4
            if request.form['action'] == 'pentagon2':
                img = 5
                
            return render_template("home.html", img = img)
        
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
    
    # doing ref like this does not work somehow, will instead refresh the path everytime it is called
    # ref = db.child('records').child(user['localId'])
    
    # if user (localId) doesn't exist
    if db.child('records').child(user['localId']).get().val() is None:
        db.child('records').child(user['localId']).set({record: data})
    # if record name already exists
    elif db.child('records').child(user['localId']).child(record).get().val():
        return True
    # if record name doesn't exist
    else:
        print("Success")
        db.child('records').child(user['localId']).child(record).set(data)


def get_last_record():
    user = auth.get_account_info(session['idToken'])['users'][0]
    ref = db.child('records').child(user['localId']).order_by_child('timestamp').limit_to_last(1)
    
    return ref.get().val()