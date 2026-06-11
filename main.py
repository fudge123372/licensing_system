from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import create_user,login_user,create_business,create_application,get_applications,approve_application,reject_application,get_my_businesses,get_my_applications,create_license,get_licenses,total_users,total_businesses,total_applications,pending_applications,approved_applications,rejected_applications,get_my_licenses

app = Flask(__name__)
app.secret_key = "qfcremiw0o323r23"


@app.route("/")
def home():

    users = total_users()
    businesses = total_businesses()
    applications = total_applications()

    return render_template("landing.html", users=users,businesses=businesses,applications=applications)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/add_user", methods=["POST"])
def add_user():
    full_name = request.form["full_name"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    password = request.form["password"]
    role = "Business Owner"
    user = (full_name,email,phone_number,password,role)

    create_user(user)
    flash("Registration successful")
    return redirect(url_for("login"))


# LOGIN

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_user", methods=["POST"])
def login_user_route():
    email = request.form["email"]
    password = request.form["password"]
    user = login_user(email, password)
    if user:

        session["user_id"] = user[0]
        session["full_name"] = user[1]
        session["role"] = user[5]
        flash("Login Successful")

        if user[5] == "Officer":
            return redirect("/officer_dashboard")
        return redirect("/dashboard")
    flash("Invalid Email or Password")
    return redirect("/login")

# LOGOUT

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged Out Successfully")
    return redirect("/")

# OWNER DASHBOARD

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    businesses = get_my_businesses(session["user_id"])
    applications = get_my_applications(session["user_id"])
    licenses = get_my_licenses(session["user_id"])
    return render_template("dashboard.html",businesses=businesses,applications=applications)

# BUSINESS REGISTRATION

@app.route("/business")
def business():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("business.html")

@app.route("/add_business", methods=["POST"])
def add_business():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    business_name = request.form["business_name"]
    business_type = request.form["business_type"]
    location = request.form["location"]

    business = (user_id,business_name,business_type,location)
    create_business(business)
    flash("Business Registered Successfully")
    return redirect("/dashboard")

# APPLY FOR LICENSE

@app.route("/apply")
def apply_license():
    if "user_id" not in session:
        return redirect("/login")
    businesses = get_my_businesses(session["user_id"])
    return render_template("apply.html",businesses=businesses)


@app.route("/create_application", methods=["POST"])
def create_application_route():
    business_id = request.form["business_id"]
    application_type = request.form["application_type"]
    application = (business_id,application_type)
    create_application(application)
    flash("Application Submitted Successfully")
    return redirect("/dashboard")

# MY APPLICATIONS
@app.route("/my_applications")
def my_applications():
    if "user_id" not in session:
        return redirect("/login")
    applications = get_my_applications(session["user_id"])

    return render_template("my_applications.html",applications=applications)

# LICENSES

@app.route("/licenses")
def licenses():
    if "user_id" not in session:
        return redirect("/login")
    licenses = get_my_licenses(session["user_id"])
    return render_template("licenses.html",licenses=licenses)


@app.route("/officer_dashboard")
def officer_dashboard():

    if session.get("role") != "Officer":
        return redirect("/")
    users = total_users()
    businesses = total_businesses()
    applications = total_applications()
    pending = pending_applications()
    approved = approved_applications()
    rejected = rejected_applications()
    return render_template("officer_dashboard.html",users=users,businesses=businesses,applications=applications,pending=pending,approved=approved,rejected=rejected)

@app.route("/applications")
def applications():
    if session.get("role") != "Officer":
        flash("Access Denied")
        return redirect("/")

    applications = get_applications()
    return render_template("officer_applications.html",applications=applications)


@app.route("/review", methods=["POST"])
def review():
    if session.get("role") != "Officer":
        flash("Access Denied")
        return redirect("/")

    application_id = request.form["application_id"]
    action = request.form["action"]
    if action == "approve":
        approve_application(application_id)
        create_license(application_id)
    elif action == "reject":
        reject_application(application_id)
    flash("Application Updated")
    return redirect("/applications")


app.run(debug=True)