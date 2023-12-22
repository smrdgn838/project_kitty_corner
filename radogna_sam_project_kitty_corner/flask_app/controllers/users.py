from flask_app import app
from flask_app.models.user import User
from flask_app.models.kitty import Kitty
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/dashboard')
def dashboard():
    if not session.get("user_id"):
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    kitties = Kitty.get_all()
    user = User.get_by_id(data)
    return render_template("dashboard.html", user=user, kitties=kitties)



@app.route('/register', methods=["POST"])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pw_hash
    }
    if User.get_by_email(data):
        flash("Email already in use!!")
        return redirect('/')
    else:
        user_id = User.create_user(data)
        session["user_id"] = user_id
        return redirect('/dashboard')


@app.route('/login', methods=["POST"])
def login():
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email and/or Password!!")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email and/or Password!!")
        return redirect('/')
    session["user_id"] = user_in_db.id
    return redirect('/dashboard')


@app.route('/corner_cafe')
def corner_cafe():
    if not session.get("user_id"):
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("corner_cafe.html", user=user)



@app.route('/corner_cafe/pix')
def corner_cafe_pix():
    if not session.get("user_id"):
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("corner_cafe_pix.html", user=user)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')