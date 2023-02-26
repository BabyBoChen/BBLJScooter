from dataclasses import asdict
import datetime
from pprint import pprint
from typing import Optional
from bblj_scooter.models.car import Car
from bblj_scooter.models.i_car_service import ICarService
from bblj_scooter.models.maintenance import Maintenance
from bblj_scooter.services.car_service import CarService
from service_container import ServiceContainer


class MaintenanceViewModel():
    def __init__(self, car_id:str):
        self.car_id = car_id
        self.service:ICarService = self.get_service()
        self.car = self.service.get_car_by_id(self.car_id)
        self.maint:Maintenance = None
        self.today = self.maint_date_to_str(datetime.datetime.now())
        return
    #######################################
    def get_service(self) -> ICarService:
        s:ICarService = ServiceContainer.get_transient(ICarService)
        return s
    #######################################
    def get_maintenance_by_id(self, maint_id:str) -> Optional[Maintenance]:
        maint = self.service.get_maintenance_by_id(self.car, maint_id)
        self.maint = maint
        return maint
    #######################################
    def maint_date_to_str(self, maint_date:datetime.datetime) -> str:
        maint_date_str = f"{maint_date.year}-{maint_date.month:02}-{maint_date.day:02}"
        return maint_date_str
    #######################################
    def map_maint(self, maint_dict) -> Maintenance:
        if self.maint is None:
            self.maint = Maintenance()
        self.maint.item_name = maint_dict["item_name"]
        self.maint.maint_date = datetime.datetime.strptime(maint_dict["maint_date"], "%Y-%m-%d")
        self.maint.mileage = int(maint_dict["mileage"])
        self.maint.price = float(maint_dict["price"])
        # pprint(asdict(self.maint))
        return self.maint
    #######################################
    def insert_maint(self, maint:Maintenance):
        self.service.insert_maint(self.car_id, maint)
        return
    #######################################
    def update_maint(self, maint:Maintenance):
        self.service.update_maint(self.car_id, maint)
        return
    #######################################
    def delete_maint(self, maint:Maintenance):
        self.service.delete_maint(self.car_id, maint)
        return
    #######################################