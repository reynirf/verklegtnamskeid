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

    def save_new_car(self, car_type, make, model, year, 
    number_of_seats, number_plate, fuel, driving_transmission):
        with open(self.VEHICLE_FILE, 'a') as vehicle_file:
            csv_writer = csv.writer(vehicle_file)
            csv_writer.writerow([car_type,make,model,year,number_of_seats,number_plate,
            fuel,driving_transmission])
    
    def delete_vehicle(self, vehicle):
        """
        Basically copy/paste from delete customer.
        """
        file_content = []
        with open(self.VEHICLE_FILE, 'r') as vehicle_file:
            csv_reader = csv.reader(vehicle_file)
            for line in csv_reader:
                if line[1] != vehicle.get_licence():
                    file_content.append(line)
        with open(self.VEHICLE_FILE, 'w', newline='') as vehicle_file:
            csv_writer = csv.writer(vehicle_file)
            for line in file_content:
                csv_writer.writerow(line)