from typing import Optional
from bblj_scooter.models.car import Car
from bblj_scooter.models.maintenance import Maintenance
import pymongo

class ICarService():

    def get_all_cars(self) -> list[Car]:
        pass
    def get_car_by_id(self, _id:str) -> Car:
        pass
    def get_maintenance_by_id(self, car_id:str, maint_id:str) -> Optional[Maintenance]:
        pass
    def map_car(self, doc_car:dict, include_maintenance:bool=False) -> Car:
        pass
    def map_maintenance(self, m:dict) -> Maintenance:
        pass
    def get_car_by_id(self, _id:str) -> Optional[Car]:
        pass
    def get_top_car(self) -> Optional[Car]:
        pass
    def move_to_top(self, _id:str) -> Optional[Car]:
        pass
    def update_car(self, car:Car):
        pass
    def delete_car(self, _id:str):
        pass
    def get_maintenance_by_id(self, car:Car, maint_id: str) -> Optional[Maintenance]:
        pass
    def insert_maint(self, car_id:str, maint:Maintenance):
        pass
    def update_maint(self, car_id:str, maint:Maintenance):
        pass
    def delete_maint(self, car_id:str, maint:Maintenance):
        pass
