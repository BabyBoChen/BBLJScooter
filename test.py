# from bblj_scooter.models.i_car_service import ICarService
# from bblj_scooter.services.car_service import CarService
# from service_container import ServiceContainer

# ServiceContainer.add_transient(ICarService, CarService)
# a:ICarService = ServiceContainer.get_transient(ICarService)
# print(a)

from app import app
app.run(host="0.0.0.0", port=8080, debug=True)

# from waitress import serve
# serve(app, host='0.0.0.0', port=8080)