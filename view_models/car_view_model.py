import datetime
from bblj_scooter.models.car import Car
from bblj_scooter.models.i_car_service import ICarService
from service_container import ServiceContainer

class CarViewModel():
    def __init__(self, _id:str) -> None:
        self.service:ICarService = self.get_service()
        self.car:Car = self.service.get_car_by_id(_id)
        return
    #######################################
    def get_service(self) -> ICarService:
        s:ICarService = ServiceContainer.get_transient(ICarService)
        return s
    #######################################
    def map_car(self, car_dict:dict) -> Car:
        self.car.plate = car_dict["plate"]
        self.car.brand = car_dict["brand"]
        self.car.model = car_dict["model"]
        self.car.year = int(car_dict["year"])
        return self.car
    #######################################
    def update_car(self, car:Car):
        self.service.update_car(car)
        return
    #######################################
    def delete_car(self):
        self.service.delete_car(self.car._id)
        return
    #######################################
    def maint_date_to_str(self, maint_date:datetime.datetime) -> str:
        maint_date_str = f"{maint_date.year}/{maint_date.month:02}/{maint_date.day:02}"
        return maint_date_str
    #######################################