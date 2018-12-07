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
                csv_reader = csv.DictReader(vehicle_file, delimiter=';')
                for line in csv_reader:
                    vehicle = Vehicle(
                        line['licence'],
                        line['make'],
                        line['model'], 
                        line['year'], 
                        line['type'],
                        line['seats'],
                        line['fuel'],
                        line['transmission'], 
                        line['maintainance'],
                        line['dates rented'])
                    self.__vehicle_list.append(vehicle)
        return self.__vehicle_list

    def save_new_car(self, number_plate, make, model, year, car_type, number_of_seats,
             fuel, driving_transmission, maintainance=0, dates_rented=[]):
        with open(self.VEHICLE_FILE, 'a') as vehicle_file:
            csv_writer = csv.writer(vehicle_file, delimiter=';')
            csv_writer.writerow([number_plate,make,model,year,car_type,number_of_seats,
            fuel,driving_transmission])
    
    def delete_vehicle(self, vehicle):
        """
        Basically copy/paste from delete customer.
        """
        file_content = []
        with open(self.VEHICLE_FILE, 'r') as vehicle_file:
            csv_reader = csv.reader(vehicle_file, delimiter=';')
            for line in csv_reader:
                if line[0] != vehicle.get_licence():
                    file_content.append(line)
        with open(self.VEHICLE_FILE, 'w', newline='') as vehicle_file:
            csv_writer = csv.writer(vehicle_file, delimiter=';')
            for line in file_content:
                csv_writer.writerow(line)