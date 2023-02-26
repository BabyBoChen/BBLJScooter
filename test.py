from bblj_scooter.models.i_car_service import ICarService
from bblj_scooter.services.car_service import CarService
from service_container import ServiceContainer

ServiceContainer.add_transient(ICarService, CarService)
a:ICarService = ServiceContainer.get_transient(ICarService)
print(a)

# python -m flask --debug run --host=0.0.0.0