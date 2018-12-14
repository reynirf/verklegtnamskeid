from models.vehicle import Vehicle
import csv


class VehicleRepo:
    VEHICLE_FILE = "./data/vehicles.csv"

    def __init__(self):
        self.__vehicle_list = []

    def get_vehicle_list(self):
        """Reads in all vehicles from the file and returns a list of Vehicle instances"""
        if self.__vehicle_list == []:
            with open(self.VEHICLE_FILE, "r") as vehicle_file:
                csv_reader = csv.DictReader(vehicle_file, delimiter=";")
                for line in csv_reader:
                    # the column for dates rented needs to be split into a list before
                    # the data is converted to a Vehicle instance
                    try:
                        dates = line["dates rented"].split(",")
                    except AttributeError:
                        dates = []
                    if line["licence"] != None:
                        vehicle = Vehicle(
                            line["licence"],
                            line["make"],
                            line["model"], 
                            line["year"], 
                            line["type"],
                            line["seats"],
                            line["fuel"],
                            line["transmission"], 
                            dates)
                        self.__vehicle_list.append(vehicle)
        return self.__vehicle_list

    def save_new_vehicle(
        self, license_plate, make, model, year, vehicle_type, 
        number_of_seats, fuel, driving_transmission, dates_rented=[]
    ):
        """Saves a new vehicle to file"""
        with open(self.VEHICLE_FILE, "a") as vehicle_file:
            csv_writer = csv.writer(vehicle_file, delimiter=";")
            csv_writer.writerow([
                license_plate,
                make,
                model,
                year,
                vehicle_type,
                number_of_seats,
                fuel,
                driving_transmission, 
                dates_rented
            ])
        self.__vehicle_list = []
    
    def delete_vehicle(self, vehicle):
        """Reads vehicles from file and compares them to the given vehicle. 
        Writes the file again without the line that matches the license plate.
        """
        file_content = []
        with open(self.VEHICLE_FILE, "r") as vehicle_file:
            csv_reader = csv.reader(vehicle_file, delimiter=";")
            for line in csv_reader:
                # compares first column of non empty lines to vehicle license plate
                if line != []:
                    if line[0] != vehicle.get_license():
                        file_content.append(line)
        with open(self.VEHICLE_FILE, "w", newline="") as updated_file:
            csv_writer = csv.writer(updated_file, delimiter=";")
            for line in file_content:
                csv_writer.writerow(line)
        self.__vehicle_list = []