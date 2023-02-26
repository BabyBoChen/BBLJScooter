from flask import Flask, render_template, request, redirect, session
from secret import *
from app import app

@app.before_request
def authorize():
    need_auth_endpoints = [
        "cars", "car", "move_to_top", "delete_car", "edit_car", "maintenance", 
        "car_maintenance", "new_maintenance", "insert_maintenance", "edit_maintenance",
        "save_maintenance", "delete_maintenance"
    ]
    if request.endpoint in need_auth_endpoints and is_login() is False:
        return redirect("/login")
    else:
        pass
    return

def is_login() -> bool:
    _is_login = False
    if "is_login" in session:
        _is_login = True
    return _is_login

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/user_login", methods=['POST'])
def user_login():
    global err_msg
    if request.form.get("password") == PASSWORD:
        session["is_login"] = True
        return redirect("/")
    else:
        err_msg = "登入失敗"
        return redirect("/error")