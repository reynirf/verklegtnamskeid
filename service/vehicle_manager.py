from repos.vehicle_repo import VehicleRepo
from models.vehicle import Vehicle

class VehicleManager:

    def __init__(self):
        self.__vehicle_repo = VehicleRepo()
    
    def get_vehicle_list(self):
        return self.__vehicle_repo.get_vehicle_list()