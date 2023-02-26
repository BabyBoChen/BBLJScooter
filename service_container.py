class _ServiceDict():
    def __init__(self, interface_class, service_class):
        self.interface_class = interface_class
        self.service_class = service_class
class ServiceContainer():
    _services:list[_ServiceDict] = []
    @staticmethod
    def add_transient(interface_class, service_class):
        ServiceContainer._services.append(_ServiceDict(interface_class, service_class))
        return    
    @staticmethod
    def get_transient(interface_class):
        service = None
        for sd in reversed(ServiceContainer._services):
            if sd.interface_class == interface_class:
                service = sd.service_class()
                break
        return service