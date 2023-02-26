from dataclasses import dataclass
from bblj_scooter.models.maintenance import Maintenance

@dataclass()
class Car():
    _id: str = ""
    plate: str = ""
    brand: str = ""
    model: str = ""
    year: int = 0
    maintenance: list[Maintenance] = None
    line_id: int = 0
