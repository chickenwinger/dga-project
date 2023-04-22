from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect,
    flash,
    session,
    Blueprint,
    current_app as app,
)
from flask_mail import Mail, Message
from dga import db, auth
import time
from collections import OrderedDict
from .auth_utils import login_required
from .dga_utils import dt1, dt4, dt5, pentagon1, pentagon2


graph = Blueprint("graph", __name__)
mail = Mail()


@graph.route("/overview", methods=["GET", "POST"])
@login_required
def overview():
    try:
        user = auth.get_account_info(session["idToken"])["users"][0]
    except:
        flash("Session expired, please login again", "error")
        return redirect(url_for("authentication.index"))

    dga_type = request.args.get("type", None)

    all_records = get_all_records(user, dga_type)
    tag_nums = []
    gas_concs = []
    tag_gas_dict = {}
    if all_records:
        tag_nums, gas_concs = all_records
        tag_gas_dict = dict(zip(tag_nums, gas_concs))
    else:
        tag_gas_dict = None

    if request.method == "POST":
        records = request.form.to_dict()

        records["timestamp"] = str(time.time())

        new_tag_no = generate_tag_number(user, dga_type)

        db.child("records").child(user["localId"]).child("2023").child(dga_type).child(
            new_tag_no
        ).set(records)

        flash("Record successfully added", "msg")
        return redirect(
            url_for(
                "graph.overview",
                type=dga_type,
                tag_gas_dict=tag_gas_dict,
                get_fault=get_fault,
            )
        )

    return render_template(
        "overview.html",
        type=dga_type,
        tag_gas_dict=tag_gas_dict,
        get_fault=get_fault,
    )


def generate_tag_number(user, dga_type):
    # prefix for the tag_no
    prefix = dga_type.upper()

    # get the last tag_no
    max_tag_no = (
        db.child("records")
        .child(user["localId"])
        .child("2023")
        .child(dga_type)
        .order_by_key()
        .limit_to_last(1)
        .get()
    )

    if max_tag_no.val() is None:  # if no records exist
        print("No records exist")
        new_tag_no = prefix + "0001"
    else:
        print("Records exist")
        current_max_tag_no = list(max_tag_no.val().keys())[0]  # type: ignore
        new_tag_no = prefix + str(int(current_max_tag_no[3:]) + 1).zfill(4)

    print(new_tag_no)
    return new_tag_no


def get_all_records(user, dga_type):
    records = (
        db.child("records").child(user["localId"]).child("2023").child(dga_type).get()
    )

    if records.val() is None or records.val() == 0:
        return None

    tag_nums = []
    gas_concs = []
    for tag_num, gas_conc in records.val().items():  # type: ignore
        tag_nums.append(tag_num)
        gas_concs.append(gas_conc)

    print(tag_nums, gas_concs)
    return tag_nums, gas_concs


def get_record(user, dga_type, tag_num):
    records = (
        db.child("records")
        .child(user["localId"])
        .child("2023")
        .child(dga_type)
        .child(tag_num)
        .get()
    )

    if records.val() is None or records.val() == 0:
        return None

    # the record in OrderedDict format
    return records.val()


def get_fault(data_type, tag_num):
    user = auth.get_account_info(session["idToken"])["users"][0]
    record = dict(get_record(user, data_type, tag_num))  # type: ignore

    if data_type == "dt1":
        ethylene = float(record["ethyleneconc"])
        methane = float(record["methaneconc"])
        acetylene = float(record["acetyleneconc"])

        fault = dt1(ethylene, methane, acetylene)
    elif data_type == "dt4":
        methane = float(record["methaneconc"])
        hydrogen = float(record["hydrogenconc"])
        ethane = float(record["ethaneconc"])

        fault = dt4(methane, hydrogen, ethane)
    elif data_type == "dt5":
        ethylene = float(record["ethyleneconc"])
        ethane = float(record["ethaneconc"])
        methane = float(record["methaneconc"])

        fault = dt5(ethylene, methane, ethane)
    elif data_type == "dp1":
        ethylene = float(record["ethyleneconc"])
        methane = float(record["methaneconc"])
        acetylene = float(record["acetyleneconc"])
        hydrogen = float(record["hydrogenconc"])
        ethane = float(record["ethaneconc"])

        fault = pentagon1(ethane, hydrogen, acetylene, ethylene, methane)
    else:
        ethylene = float(record["ethyleneconc"])
        methane = float(record["methaneconc"])
        acetylene = float(record["acetyleneconc"])
        hydrogen = float(record["hydrogenconc"])
        ethane = float(record["ethaneconc"])

        fault = pentagon2(ethane, hydrogen, acetylene, ethylene, methane)

    return fault
