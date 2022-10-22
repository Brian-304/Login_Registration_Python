from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index_page():
    session.clear()
    return render_template("register.html")

@app.route("/users/register", methods=["POST"])
def register_user():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    
    data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    
    user_id = User.save(data)
    print(f"user id is {str(user_id)}")
    
    session["user_id"] = user_id
    return redirect("/main")
    
@app.route("/users_login", methods=["POST"])
def login_user():
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    
    if not user_in_db:
        flash("Invalid email")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid password")
        return redirect("/")
    session["user_id"] = user_in_db.id
    return redirect("/main")
    
@app.route("/main")
def main_page():
    if session.get("user_id") == None:
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    logged_user = User.get_by_id(data)
    return render_template("main.html", logged_user=logged_user)

@app.route("/logout")
def logout_user():
    return redirect("/main")