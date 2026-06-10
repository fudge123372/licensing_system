from flask import Flask,render_template,request,redirect,url_for,flash,session
from database import create_user,login_user

app=Flask(__name__)

app.secret_key="qfcremiw0o323r23"

@app.route("/")#decorator funtion
def home():#view funtions
    return render_template("dashboard.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add_user",methods=["POST"])
def add_user():
    full_name=request.form["full_name"]
    email=request.form["email"]
    phone_number=request.form["phone_number"]
    password=request.form["password"]
    role=request.form["role"]

    user=(full_name,email,phone_number,password,role)

    create_user(user)
    flash("Registration successful")
    return redirect(url_for("register"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_user", methods=["POST"])
def login_user_route():

    email = request.form["email"]
    password = request.form["password"]

    user = login_user(email, password)

    if user:
        return redirect("/")

    flash("Invalid email or password")
    return redirect("/login")


app.run(debug=True)