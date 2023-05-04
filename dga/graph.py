from flask import (
    Flask,
    jsonify,
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

dga_type = None


@graph.route("/overview", methods=["GET", "POST"])
@login_required
def overview():
    try:
        user = auth.get_account_info(session["idToken"])["users"][0]
    except:
        flash("Session expired, please login again", "error")
        return redirect(url_for("authentication.index"))

    global dga_type
    dga_type = request.args.get("type", None)

    breadcrumb_items = [
        {
            "url": url_for("graph.overview", type="dt1"),
            "text": "Duval Triangle 1",
            "active": True if dga_type == "dt1" else False,
        },
        {
            "url": url_for("graph.overview", type="dt4"),
            "text": "Duval Triangle 4",
            "active": True if dga_type == "dt4" else False,
        },
        {
            "url": url_for("graph.overview", type="dt5"),
            "text": "Duval Triangle 5",
            "active": True if dga_type == "dt5" else False,
        },
        {
            "url": url_for("graph.overview", type="dp1"),
            "text": "Duval Pentagon 1",
            "active": True if dga_type == "dp1" else False,
        },
        {
            "url": url_for("graph.overview", type="dp2"),
            "text": "Duval Pentagon 2",
            "active": True if dga_type == "dp2" else False,
        },
    ]

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
                get_fault=get_fault,
                breadcrumb_items=breadcrumb_items,
            )
        )

    return render_template(
        "overview.html",
        type=dga_type,
        get_fault=get_fault,
        breadcrumb_items=breadcrumb_items,
    )


@app.route("/get_table_data")
def data():
    user = auth.get_account_info(session["idToken"])["users"][0]
    print(dga_type)  # type: ignore

    all_records = get_all_records(user, dga_type)

    # Prepare the data in the required format
    result = []
    if all_records:
        for tag_num, gas_conc in all_records.items():  # type: ignore
            record = {"tag_num": tag_num}
            gaseous = {"gaseous_content": gas_conc}
            record.update(gaseous)
            fault = get_fault(dga_type, tag_num)
            fault = {"fault": fault}
            record.update(fault)
            result.append(record)

    print(result)
    json_result = jsonify(result)
    print(json_result)
    return json_result


@graph.route("/records", methods=["GET", "POST"])
@login_required
def records():
    return render_template("records.html")


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

    return records.val()


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


def extract_gases(record, data_type):
    gases = {}
    required_gases = {
        "dt1": ["ethyleneconc", "methaneconc", "acetyleneconc"],
        "dt4": ["methaneconc", "hydrogenconc", "ethaneconc"],
        "dt5": ["ethyleneconc", "methaneconc", "ethaneconc"],
        "dp1": [
            "ethyleneconc",
            "methaneconc",
            "acetyleneconc",
            "hydrogenconc",
            "ethaneconc",
        ],
        "dp2": [
            "ethyleneconc",
            "methaneconc",
            "acetyleneconc",
            "hydrogenconc",
            "ethaneconc",
        ],
    }

    for gas in required_gases[data_type]:
        gases[gas] = float(record.get(gas, 0))

    return gases


def get_fault(data_type, tag_num):
    user = auth.get_account_info(session["idToken"])["users"][0]
    record = dict(get_record(user, data_type, tag_num))  # type: ignore
    fault = None

    gases = extract_gases(record, data_type)

    if data_type == "dt1":
        fault = dt1(gases["ethyleneconc"], gases["methaneconc"], gases["acetyleneconc"])
    elif data_type == "dt4":
        fault = dt4(gases["methaneconc"], gases["hydrogenconc"], gases["ethaneconc"])
    elif data_type == "dt5":
        fault = dt5(gases["ethyleneconc"], gases["methaneconc"], gases["ethaneconc"])
    elif data_type == "dp1":
        fault = pentagon1(
            gases["ethaneconc"],
            gases["hydrogenconc"],
            gases["acetyleneconc"],
            gases["ethyleneconc"],
            gases["methaneconc"],
        )
    else:
        fault = pentagon2(
            gases["ethaneconc"],
            gases["hydrogenconc"],
            gases["acetyleneconc"],
            gases["ethyleneconc"],
            gases["methaneconc"],
        )

    return fault
