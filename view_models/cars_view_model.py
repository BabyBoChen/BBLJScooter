from bblj_scooter.models.car import Car
from bblj_scooter.models.i_car_service import ICarService
from bblj_scooter.services.car_service import CarService
from service_container import ServiceContainer

class CarsViewModel():
    def __init__(self) -> None:
        self.service:ICarService = self.get_service()
        self.cars:list[Car] = self.service.get_all_cars()
        return
    #######################################
    def get_service(self) -> ICarService:
        s:ICarService = ServiceContainer.get_transient(ICarService)
        return s
    #######################################
    def move_to_top(self, _id:str) -> None:
        self.service.move_to_top(_id)
        self.cars = self.service.get_all_cars()
        return
    #######################################