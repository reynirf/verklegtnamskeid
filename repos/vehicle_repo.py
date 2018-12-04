from models.vehicle import Vehicle
import csv

class VehicleRepo:

    VEHICLE_FILE = "./data/vehicles.csv"

    def __init__(self):
        self.__vehicle_list = []

    def get_vehicle_list(self):
        """Returns a list of all vehicles on file"""
        if self.__vehicle_list == []:
            with open(self.VEHICLE_FILE, 'r') as vehicle_file:
                csv_reader = csv.DictReader(vehicle_file)
                for line in csv_reader:
                    vehicle = Vehicle(
                        line['licence'],
                        line['make'], 
                        line['year'], 
                        line['type'],
                        line['color'],
                        line['seats'], 
                        line['maintainance'])
                    self.__vehicle_list.append(vehicle)
        return self.__vehicle_list