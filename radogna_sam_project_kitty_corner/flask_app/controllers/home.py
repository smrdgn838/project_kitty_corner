from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def home():
    if session.get('user_id'):
        return redirect ('/dashboard')        
    return render_template("home.html")



