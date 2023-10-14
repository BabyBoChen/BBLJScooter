import service_injection as _

from flask import Flask, render_template, request, redirect
from view_models.cars_view_model import CarsViewModel
from view_models.car_view_model import CarViewModel
from view_models.maintenance_view_model import MaintenanceViewModel
from secret import *

app = Flask(__name__, static_folder="wwwroot", template_folder="views")
app.secret_key = SECRET_KEY
err_msg = ""

import middleware_authorize as _

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/cars")
def cars():
    global err_msg
    try:
        vm = CarsViewModel()
        return render_template("cars.html", model=vm)
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/car/<car_id>")
def car(car_id=None):
    global err_msg
    try:
        vm = CarViewModel(car_id)
        return render_template("car.html", model=vm)
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/move_to_top/<car_id>")
def move_to_top(car_id=None):
    global err_msg
    try:
        vm = CarsViewModel()
        vm.move_to_top(car_id)
        return render_template("cars.html", model=vm)
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/delete_car/<car_id>")
def delete_car(car_id=None):
    global err_msg
    try:
        vm = CarViewModel(car_id)
        vm.delete_car()
        return redirect("/cars")
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/edit_car/<car_id>", methods=['POST'])
def edit_car(car_id=None):
    global err_msg
    try:
        car_dict = {
            "plate" : request.form.get("plate"),
            "brand" : request.form.get("brand"),
            "model" : request.form.get("model"),
            "year" : request.form.get("year"),
        }
        vm = CarViewModel(car_id)
        car = vm.map_car(car_dict)
        vm.update_car(car)
        return redirect("/cars")
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/maintenance")
def maintenance():
    global err_msg
    try:
        vm = CarsViewModel()
        return render_template("maintenance.html", model=vm)
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/car_maintenance/<car_id>")
def car_maintenance(car_id=None):
    global err_msg
    try:
        vm = CarViewModel(car_id)
        return render_template("car_maintenance.html", model=vm)
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/new_maintenance/<car_id>")
def new_maintenance(car_id=None):
    global err_msg
    try:
        vm = MaintenanceViewModel(car_id)
        return render_template("new_maintenance.html", model=vm)
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/insert_maintenance", methods=['POST'])
def insert_maintenance():
    global err_msg
    try:
        car_id = request.form.get("car_id")
        maint_dict = {
            "maint_date" : request.form.get("maint_date"),
            "item_name" : request.form.get("item_name"),
            "mileage" : request.form.get("mileage"),
            "price" : request.form.get("price"),
        }
        vm = MaintenanceViewModel(car_id)
        maint = vm.map_maint(maint_dict)
        vm.insert_maint(maint)
        return redirect(f"/car_maintenance/{car_id}")
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")


@app.route("/edit_maintenance/<car_id>/<maint_id>")
def edit_maintenance(car_id:str=None, maint_id:str=None):
    global err_msg
    try:
        vm = MaintenanceViewModel(car_id)
        vm.get_maintenance_by_id(maint_id)
        return render_template("edit_maintenance.html", model=vm)
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/save_maintenance", methods=['POST'] )
def save_maintenance():
    global err_msg
    try:
        car_id = request.form.get("car_id")
        maint_id = request.form.get("_id")
        maint_dict = {
            "maint_date" : request.form.get("maint_date"),
            "item_name" : request.form.get("item_name"),
            "mileage" : request.form.get("mileage"),
            "price" : request.form.get("price"),
        }
        vm = MaintenanceViewModel(car_id)
        vm.get_maintenance_by_id(maint_id)
        maint = vm.map_maint(maint_dict)
        vm.update_maint(maint)
        return redirect(f"/car_maintenance/{car_id}")
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/delete_maintenance/<car_id>/<maint_id>")
def delete_maintenance(car_id:str=None, maint_id:str=None):
    global err_msg
    try:
        vm = MaintenanceViewModel(car_id)
        maint = vm.get_maintenance_by_id(maint_id)
        vm.delete_maint(maint)
        return redirect(f"/car_maintenance/{car_id}")
    except Exception as ex:
        err_msg = str(ex)
        return redirect("/error")

@app.route("/error")
def error():
    global err_msg
    return render_template("error.html", err_msg=err_msg)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)
