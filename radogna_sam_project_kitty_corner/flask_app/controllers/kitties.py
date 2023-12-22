from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.kitty import Kitty


@app.route('/kitty/new')
def new_kitty():
    if not session.get("user_id"):
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user = User.get_by_id(data)
    return render_template("new_kitty.html",  user=user)


@app.route('/kitty/create', methods=["POST"])
def create_kitty():
    if not Kitty.validate_kitty(request.form):
        return redirect('/kitty/new')
    else:
        Kitty.create_kitty(request.form)
        return redirect('/dashboard')
    

# @app.route('/kitty/<int:id>')
# def kitty_get(id):
#     data = {
#         "id": id,
#         "user_id": session["user_id"]
#     }
#     kitty = Kitty.get_by_id(data)
#     return render_template("view_kitty.html", kitty=kitty)


@app.route('/kitty/edit/<int:id>')
def edit_kitty(id):
    data = {
        "id": id
    }
    kitty = Kitty.get_by_id(data)
    user = User.get_by_id(data)
    return render_template("edit_kitty.html", kitty=kitty, user=user)


@app.route('/kitty/update', methods=["POST"])
def update_kitty():
    id = request.form.get("id")
    if not Kitty.validate_kitty(request.form):
        return redirect(f'/kitty/edit/{id}')
    else:
        data = {
            "id": id,
            "age_range": request.form["age_range"],
            "breed": request.form["breed"],
            "personality": request.form["personality"],
            "other_pets": request.form["other_pets"]
        }
        Kitty.update_kitty(data)
        return redirect('/dashboard')



@app.route('/kitty/delete/<int:id>')
def delete_kitty(id):
    data = {
        "id": id
    }
    Kitty.delete_kitty(data)
    return redirect('/dashboard')



