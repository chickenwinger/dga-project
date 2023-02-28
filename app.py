from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/records")
def records():
    return render_template("records.html")


if __name__ == "__main__":
    app.run(debug=True)