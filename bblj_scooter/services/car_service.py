from dataclasses import asdict
from pprint import pprint
from typing import Optional
from bblj_scooter.models.car import Car
from bblj_scooter.models.i_car_service import ICarService
from bson.objectid import ObjectId
import pymongo

from bblj_scooter.models.maintenance import Maintenance
from bblj_scooter.services.db_secret import CONN_STRING

class CarService(ICarService):
    _conn:pymongo.MongoClient = pymongo.MongoClient(CONN_STRING)
    _conn._timeout = 30.0
    #######################################
    @staticmethod
    def get_connection() -> pymongo.MongoClient:
        try:
            CarService._conn.server_info()
        except Exception:
            CarService._conn = pymongo.MongoClient(CONN_STRING)
            CarService._conn._timeout = 30.0
        return CarService._conn
    #######################################
    def __init__(self) -> None:
        return
    #######################################
    def get_all_cars(self) -> list[Car]:
        cars = []
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        doc_cars = col_cars.find().sort("line_id", -1)
        for doc_car in doc_cars:
            car = self.map_car(doc_car, False)
            cars.append(car)
        return cars
    #######################################
    def map_car(self, doc_car:dict, include_maintenance:bool=False) -> Car:
        car = Car()
        car._id = str(doc_car["_id"])
        car.plate = doc_car["plate"]
        car.brand = doc_car["brand"]
        car.model = doc_car["model"]
        car.year = doc_car["year"]
        car.line_id = doc_car["line_id"]
        car.maintenance = []
        if include_maintenance == True:
            try:
                has_maints = doc_car.get("maintenance") is not None
                is_list = hasattr(type(doc_car.get("maintenance")), '__iter__')
                if has_maints and is_list:
                    for m in doc_car["maintenance"]:
                        maint = self.map_maintenance(m)
                        car.maintenance.append(maint)
                    car.maintenance.sort(reverse=True, key=lambda m : m.maint_date)
            except Exception as ex:
                car.maintenance = []
        return car
    #######################################
    def map_maintenance(self, m:dict) -> Maintenance:
        maint = Maintenance()
        maint._id = str(m["_id"])
        maint.item_name = m["item_name"]
        maint.mileage = m["mileage"]
        maint.price = m["price"]
        maint.maint_date = m["maint_date"]
        return maint
    #######################################
    def get_car_by_id(self, _id:str) -> Optional[Car]:
        car = None
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        doc_car = col_cars.find_one({"_id": ObjectId(_id) })
        if doc_car is not None:
            car = self.map_car(doc_car, True)
        return car
    #######################################
    def get_top_car(self) -> Optional[Car]:
        car:Car = None
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        doc_cars = col_cars.find().sort("line_id", -1).limit(1)
        for doc_car in doc_cars:
            car = self.map_car(doc_car)
            break
        return car
    #######################################
    def move_to_top(self, _id:str) -> Optional[Car]:
        moving_car:Car = None
        max_line_id = 0
        top_car = self.get_top_car()
        if top_car is not None:
            max_line_id = top_car.line_id
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        query = { "_id" : ObjectId(_id) }
        command = { "$set" : { "line_id" : max_line_id+1 } }
        col_cars.update_one(query, command)
        moving_car = self.get_car_by_id(_id)
        return moving_car
    #######################################
    def update_car(self, car:Car):
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        query = { "_id" : ObjectId(car._id) }
        command = {"$set" : {
            "plate" : car.plate,
            "brand" : car.brand,
            "model" : car.model,
            "year" : car.year,
        } }
        col_cars.update_one(query, command)
        return
    #######################################
    def delete_car(self, _id:str):
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        col_cars.delete_one({ "_id" : ObjectId(_id) })
        return
    #######################################
    def get_maintenance_by_id(self, car:Car, maint_id: str) -> Optional[Maintenance]:
        maint:Maintenance = None
        if car is not None:
            maints = car.maintenance
            for m in maints:
                if m._id == maint_id:
                    maint = m
        return maint
    #######################################
    def insert_maint(self, car_id:str, maint:Maintenance):
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        col_cars.update_one({"_id" : ObjectId(car_id)}, {"$push" : { "maintenance" : {
            "maint_date" : maint.maint_date,
            "item_name" : maint.item_name,
            "mileage" : maint.mileage,
            "price" : maint.price,
            "_id" : ObjectId(),
        } } })
        return
    #######################################
    def update_maint(self, car_id:str, maint:Maintenance):
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        col_cars.update_one({"_id" : ObjectId(car_id), "maintenance._id" : ObjectId(maint._id)}, {"$set" : { "maintenance.$" : {
            "_id" : ObjectId(maint._id),
            "maint_date" : maint.maint_date,
            "item_name" : maint.item_name,
            "mileage" : maint.mileage,
            "price" : maint.price,
        } } })
        return
    #######################################
    def delete_maint(self, car_id:str, maint:Maintenance):
        db = CarService.get_connection()["bblj_scooter"]
        col_cars = db["cars"]
        col_cars.update_one({"_id" : ObjectId(car_id) }, {"$pull" : { "maintenance" : {
            "_id" : ObjectId(maint._id),
        } } })
        return
    #######################################    