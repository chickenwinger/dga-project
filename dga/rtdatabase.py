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
)
from flask_mail import Mail, Message
from dga import db, auth
import time
from .auth_utils import login_required
from .dga_utils import dt1, dt4, dt5, pentagon1, pentagon2

rtdatabase = Blueprint("rtdatabase", __name__)
mail = Mail()


@rtdatabase.route("/home", methods=["GET", "POST"])
@login_required
def home():
    try:
        user = auth.get_account_info(session["idToken"])["users"][0]
    except:
        flash("Session expired, please login again", "error")
        return redirect(url_for("authentication.index"))

    image_paths = ["dt1", "dt4", "dt5", "dp1", "dp2"]
    transformers = []

    transformers_path = db.child("records").child(user["localId"]).get()
    if transformers_path.val() is not None:
        for transformer in transformers_path.each():
            transformers.append(transformer.key())

    if request.method == "POST":
        if request.form["transformerRadio"] != "":
            add_record(user, request.form["transformerRadio"])

            # add record to the database
            flash("Record added successfully", "msg")
            return redirect(url_for("rtdatabase.home"))

    return render_template(
        "home.html", image_paths=image_paths, transformers=transformers
    )


@rtdatabase.route("/records", methods=["GET", "POST"])  # type: ignore
@login_required
def records():
    try:
        user = auth.get_account_info(session["idToken"])["users"][0]
    except:
        flash("Session expired, please login again", "error")
        return redirect(url_for("authentication.index"))

    image_paths = ["dt1", "dt4", "dt5", "dp1", "dp2"]
    transformers = []

    transformers_path = db.child("records").child(user["localId"]).get()
    if transformers_path.val() is not None:
        for transformer in transformers_path.each():
            transformers.append(transformer.key())

    if request.method == "POST":
        action = request.form.get("type", None)
        transformer_selected = request.form.get("transformer_selected", None)
        print(action)
        print(transformer_selected)

        if request.form.get("action") == "add":
            transformer_name = request.form.get("transformer", None)
            print(transformer_name)

            if transformers_path is None:
                db.child("records").child(user["localId"]).set({transformer_name: ""})
            else:
                db.child("records").child(user["localId"]).child(transformer_name).set(
                    ""
                )

            return redirect(url_for("rtdatabase.records"))

        elif action == "update":
            record_selected = request.form.get("record_selected", None)

            keys_and_timestamps = display_records(user, transformer_selected)
            print(keys_and_timestamps)

            if record_selected:
                data = (
                    db.child("records")
                    .child(user["localId"])
                    .child(transformer_selected)
                    .child(record_selected)
                    .child("gaseous_data")
                    .get()
                    .val()
                )

                acetylene = int(data["acetylene"])
                ethane = int(data["ethane"])
                ethylene = int(data["ethylene"])
                hydrogen = int(data["hydrogen"])
                methane = int(data["methane"])

                dt1(ethylene, methane, acetylene)
                dt4(methane, hydrogen, ethane)
                dt5(ethylene, methane, ethane)
                pentagon1(ethylene, methane, ethane, hydrogen, acetylene)
                pentagon2(ethylene, methane, ethane, hydrogen, acetylene)

            return jsonify({"kt": keys_and_timestamps})

    # if request.method == "POST":
    #     if record_selected is None:
    #         flash("Please select a record", "error")
    #         return render_template("records.html", kt=keys_and_timestamps)

    #     if request.form["action"] == "delete":
    #         # print("Delete button pressed")
    #         db.child("records").child(user["localId"]).child(record_selected).remove()

    #         flash(f"{record_selected} deleted successfully", "msg")
    #         return redirect(url_for("rtdatabase.records"))

    #     else:
    #         query_dict = dict(get_record(user, record_selected))

    #         if request.form["action"] == "email":
    #             email = auth.get_account_info(session["idToken"])["users"][0]["email"]
    #             message = Message("Hello", recipients=[email])
    #             message_body = f"Hello, this is the results of your analysis from the record named \"{record_selected}\":\n"

    #             for key, value in query_dict.items():
    #                 message_body += f"{key}: {value}\n"

    #             with app.open_resource("static/images/dt1.png") as fp:
    #                 message.attach("triangle1.png", "image/png", fp.read())
    #             with app.open_resource("static/images/dt4.png") as fp:
    #                 message.attach("triangle1.png", "image/png", fp.read())
    #             with app.open_resource("static/images/dt5.png") as fp:
    #                 message.attach("triangle1.png", "image/png", fp.read())
    #             with app.open_resource("static/images/dp1.png") as fp:
    #                 message.attach("triangle1.png", "image/png", fp.read())
    #             with app.open_resource("static/images/dp2.png") as fp:
    #                 message.attach("triangle1.png", "image/png", fp.read())

    #             message.body = message_body

    #             mail.send(message)
    #             flash("Records sent to email", "msg")

    #         else:
    #             print(query_dict)

    #             hydrogen = int(query_dict["hydrogen"])
    #             methane = int(query_dict["methane"])
    #             acetylene = int(query_dict["acetylene"])
    #             ethylene = int(query_dict["ethylene"])
    #             ethane = int(query_dict["ethane"])
    #             cmonoxide = int(query_dict["cmonoxide"])
    #             cdioxide = int(query_dict["cdioxide"])

    #             img = None
    #             fault_type = None
    #             selected_val = None
    #             if request.form["action"] == "triangle1":
    #                 img = 1
    #                 fault_type = dt1(ethylene, methane, acetylene)
    #                 selected_val = "triangle1"
    #             elif request.form["action"] == "triangle4":
    #                 img = 2
    #                 fault_type = dt4(methane, hydrogen, ethane)
    #                 selected_val = "triangle4"
    #             elif request.form["action"] == "triangle5":
    #                 img = 3
    #                 fault_type = dt5(ethylene, methane, ethane)
    #                 selected_val = "triangle5"
    #             elif request.form["action"] == "pentagon1":
    #                 img = 4
    #                 fault_type = pentagon1(ethane, hydrogen, acetylene, ethylene, methane)
    #                 selected_val = "pentagon1"
    #             elif request.form["action"] == "pentagon2":
    #                 img = 5
    #                 fault_type = pentagon2(ethane, hydrogen, acetylene, ethylene, methane)
    #                 selected_val = "pentagon2"

    #             return render_template(
    #                 "records.html",
    #                 img=img,
    #                 fault=fault_type,
    #                 selected_val=selected_val,
    #                 kt=keys_and_timestamps,
    #                 record_selected=record_selected,
    #             )

    return render_template(
        "records.html",
        image_paths=image_paths,
        transformers=transformers,
    )


def get_current_user():
    try:
        return auth.get_account_info(session["idToken"])["users"][0]
    except:
        flash("Session expired, please login again", "error")
        return redirect(url_for("authentication.index"))


def get_transformer_data(user, transformer):
    path = db.child("records").child(user["localId"]).child("transformers").get()

    return path


def add_record(user, transformer):
    new_tag_no = generate_tag_number(user, transformer)
    records = request.form.to_dict()
    ethane = int(records["ethane"])
    hydrogen = int(records["hydrogen"])
    methane = int(records["methane"])
    acetylene = int(records["acetylene"])
    ethylene = int(records["ethylene"])
    cmonoxide = int(records["cmonoxide"])
    cdioxide = int(records["cdioxide"])

    dp1 = pentagon1(ethane, hydrogen, acetylene, ethylene, methane)
    dp2 = pentagon2(ethane, hydrogen, acetylene, ethylene, methane)

    data = {
        "timestamp": time.time(),  # firebase.database.ServerValue.TIMESTAMP,
        "gaseous_data": {
            "hydrogen": hydrogen,
            "methane": methane,
            "acetylene": acetylene,
            "ethylene": ethylene,
            "ethane": ethane,
            "cmonoxide": cmonoxide,
            "cdioxide": cdioxide,
        },
        "fault_type": {
            "dt1": dt1(ethylene, methane, acetylene),
            "dt4": dt4(methane, hydrogen, ethane),
            "dt5": dt5(ethylene, methane, ethane),
        },
    }

    # doing ref like this does not work somehow, will instead refresh the path everytime it is called
    # ref = db.child('records').child(user['localId'])

    ref_path = db.child("records").child(user["localId"]).child(transformer).get()

    # if user (localId) doesn't exist
    if ref_path.val() is None:
        db.child("records").child(user["localId"]).child(transformer).set(
            {new_tag_no: data}
        )
    # for new record
    else:
        print("Successfully added record")
        db.child("records").child(user["localId"]).child(transformer).child(
            new_tag_no
        ).set(data)


def display_records(user, transformer):
    try:
        all_records = (
            db.child("records").child(user["localId"]).child(transformer).get()
        )
        keys = [record.key() for record in all_records.each()]  # type: ignore
        timestamps = [time.ctime(record.val()["timestamp"]) for record in all_records.each()]  # type: ignore

        keys_and_timestamps = dict(zip(keys, timestamps))
    except:
        keys_and_timestamps = {"No records found": ""}

    return keys_and_timestamps


def generate_tag_number(user, transformer):
    # get the last tag_no
    max_tag_no = (
        db.child("records")
        .child(user["localId"])
        .child(transformer)
        .order_by_key()
        .limit_to_last(1)
        .get()
    )

    if max_tag_no.val() is None:  # if no records exist
        print("No records exist")
        new_tag_no = "DGA" + "0001"
    else:
        current_max_tag_no = list(max_tag_no.val().keys())[0]  # type: ignore
        print(current_max_tag_no)
        new_tag_no = "DGA" + str(int(current_max_tag_no[3:]) + 1).zfill(4)

    print(new_tag_no)
    return new_tag_no


# Note to self:
# There are 2 ways to pass data in url:
# 1. using query string where the data is passed in the url itself, with ? and & as delimiters
# and the data is passed as key=value pairs in url_for(), and then using request.args.get() to get the data
# 2. using name of <input> where the data is passed in the form of <variable> in the url and the function
# must take in the variable as a parameter
