from repos.vehicle_repo import VehicleRepo
from models.vehicle import Vehicle
import string
class VehicleManager:

    def __init__(self):
        self.__vehicle_repo = VehicleRepo()
        self.__temp_car_type = ""
        self.__temp_make = ""
        self.__temp_model = ""
        self.__temp_year = ""
        self.__temp_number_of_seats = ""
        self.__temp_number_plate = ""
        self.__temp_fuel = ""
        self.__temp_driving_transmission = ""
    
    def get_vehicle_list(self):
        return self.__vehicle_repo.get_vehicle_list()

    def save_new_car(self):
        #uses the temp values to save the new customer and then clears them 
        self.__vehicle_repo.save_new_car(
            self.__temp_car_type,
            self.__temp_make,
            self.__temp_model,
            self.__temp_year,
            self.__temp_number_of_seats,
            self.__temp_number_plate,
            self.__temp_fuel,
            self.__temp_driving_transmission)

    def check_type(self,car_type):
        """check if type is valid. Returns an error message if type
        has numbers or punctuation in it"""

        for letter in car_type.strip():
            if letter in (string.digits + string.punctuation):
                return "Car type not valid. Please try again."
        self.__temp_car_type = car_type

    def check_make(self,make):
        """check if make is valid. Returns an error message if make
        has numbers or punctuation in it"""

        for letter in make.strip():
            if letter in (string.digits + string.punctuation):
                return "Make not valid. Please try again."
        self.__temp_make = make
    
    def check_model(self,model):
        self.__temp_model = model

    def check_year(self,year):
        """Check if year is valid. Returns an error message if year
        has letters or punctuation in it"""

        year = year.replace("-", "")
        for letter in year:
            if letter in (string.ascii_letters + string.punctuation) or year.strip() == '':
                return "Year not valid. Please try again."
        self.__temp_year = year

    def check_number_of_seats(self,number_of_seats):
        """Check if number of seats is valid. Returns an error message if number of seats
        has letters or punctuation in it"""

        number_of_seats = number_of_seats.replace("-", "")
        for letter in number_of_seats:
            if letter in (string.ascii_letters + string.punctuation) or number_of_seats.strip() == '':
                return "Number of seats not valid. Please try again."
        self.__temp_number_of_seats = number_of_seats

    def check_number_plate(self,number_plate):
        self.__temp_number_plate = number_plate

    def check_fuel(self,fuel):
        self.__temp_fuel = fuel

    def check_driving_transmission(self,driving_transmission):
        self.__temp_driving_transmission = driving_transmission
    
    def find_car_by_number_plate(self, number_plate):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        cars = []
        for vehicle in cars_list:
            car_licence = vehicle.get_licence().lower()
            if car_licence == number_plate.lower():
                cars.append(vehicle)
        if cars != []:
            return cars

    def find_car_by_number_make(self, make):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        cars = []
        for car in cars_list:
            if car.__str__().lower == make.lower():
                cars.append(car)
        if cars != []:
            return cars

    def find_car_by_car_type(self, type_of_car):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        cars = []
        for car in cars_list:
            if car.__str__().lower == type_of_car.lower():
                cars.append(car)
        if cars != []:
            return cars
    