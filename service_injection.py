from service_container import ServiceContainer
from bblj_scooter.models.i_car_service import ICarService
from bblj_scooter.services.car_service import CarService

ServiceContainer.add_transient(ICarService, CarService)