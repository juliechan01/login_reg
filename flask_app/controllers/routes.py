from flask import Flask, render_template, request, redirect, session
from flask_app import app
from flask_app.models.user import User

# HOMEPAGE

@app.route('/')
def home():
    return render_template("login.html")

# CREATE USER

@app.route('/register', methods=['POST'])
def register():
    if User.create_user(request.form):
        print("end")
        return redirect('/users/profile')
    return redirect('/')

# READ USER

@app.route('/users/profile')
def profile():
    return render_template("profile.html")
    flash("Login successful.")

@app.route('/users/logout')
def sign_out():
    session.clear()
    return redirect('/')
    flash("You have you been logged out.")

@app.route('/users/login', methods=['POST'])
def sign_in():
    if User.login(request.form):
        return redirect('/users/profile')
    session['user_id'] = User.id
    return redirect('/')