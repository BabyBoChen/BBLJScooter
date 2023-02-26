from dataclasses import dataclass
import datetime

@dataclass()
class Maintenance():
    _id:str = ""
    line_id:int = 0
    item_name:str = ""
    mileage:int = 0
    price:float = 0.0
    maint_date:datetime.datetime = None