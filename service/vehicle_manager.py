from repos.vehicle_repo import VehicleRepo
import datetime
from models.vehicle import Vehicle
import string
import time

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
        car_types = ["sedan", "offroad", "smallcar","bus"]
        """Check if type is valid. Returns an error message if type
        has numbers or punctuation in it"""
        inputed_car = ""
        if car_type.strip() == '':
            return self.error("Car type")
        for letter in car_type.strip():
            if letter.isalpha():
                inputed_car += letter
            elif letter == "":
                pass
            else:
                return self.error("Car type")
        
        if inputed_car in car_types:
            self.__temp_car_type = inputed_car
        else:
            return self.vehicle_type()

        """
        for letter in car_type.strip():
            if letter in (string.digits + string.punctuation):
                return self.error('Car type')
        self.__temp_car_type = car_type
        """

    def check_make(self,make):
        """Check if make is valid. Returns an error message if make
        has numbers or punctuation in it"""

        if make.strip() == '':
            return self.error("Make")

        for letter in make.strip():
            if letter in (string.digits + string.punctuation):
                return self.error('Make')
        self.__temp_make = make
    
    def check_model(self,model):
        if model.strip() == '':
            return self.error("Model")
        self.__temp_model = model

    def check_year(self,year):
        OLDEST_CAR = 1940
        present_year = datetime.datetime.today().year
        """Check if year is valid. Returns an error message if year
        has letters or punctuation in it"""

        year = year.replace("-", "")
        if year.strip() == '':
            return self.error("Year")
        year_int = ""
        for letter in year:
            if letter.isdigit():
                year_int += letter
            else:
                return self.error("Year")
        if int(year_int) > present_year:
            return self.newer(present_year)
        elif int(year_int) < OLDEST_CAR:
            return self.older(OLDEST_CAR)
        else:
            self.__temp_year = year

        # older code, i am keeping it just in case the team is not convinced
        # for letter in year:
        #    if letter in (string.ascii_letters + string.punctuation):
        #        return self.error('Year')
        # self.__temp_year = year

    def check_number_of_seats(self,number_of_seats):
        """Check if number of seats is valid. Returns an error message if number of seats
        has letters or punctuation in it"""

        if number_of_seats.strip() == '':
            return self.error("Number of seats")
        number_of_seats = number_of_seats.replace("-", "")
        seats_int = ""
        for letter in number_of_seats:
            if letter.isdigit():
                seats_int += letter
            else:
                return self.error("Number of seats")
        if int(seats_int) < 1 or int(seats_int) > 15:
            return self.nr_seats()
            time.sleep(2)
        else:
            self.__temp_number_of_seats = number_of_seats

        """
        will discuss tomorrow if it is better like this or not
        for letter in number_of_seats:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error('Number of seats')
        self.__temp_number_of_seats = number_of_seats
        """

    def check_number_plate(self,number_plate):
        """Check if number plate is valid. Returns an error message if number plate
        has punctuation in it"""

        if number_plate.strip() == '':
            return self.error("Number plate")

        for letter in number_plate:
            if letter in (string.punctuation):
                return self.error('Number of seats')
        self.__temp_number_plate = number_plate

    def check_fuel(self,fuel):
        if fuel.strip() == '':
            return self.error("Fuel")
        self.__temp_fuel = fuel

    def check_driving_transmission(self,driving_transmission):
        if driving_transmission.strip() == '':
            return self.error("Driving transmission")
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

    def find_car_by_make(self, make):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        cars = []
        for vehicle in cars_list:
            car_make = vehicle.get_make().lower()
            if car_make == make.lower():
                cars.append(vehicle)
        if cars != []:
            return cars

    def find_car_by_type(self, type_of_car):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        cars = []
        for vehicle in cars_list:
            car_type = vehicle.get_vehicle_type().lower()
            if car_type == type_of_car.lower():
                cars.append(vehicle)
        if cars != []:
            return cars

    def error(self, input_type):
        return '{} not valid. Please try again.'.format(input_type)
    
    def newer(self,year_inputed):
        return 'Year not valid. Please do not enter newer car than {}.'.format(year_inputed)

    def older(self,year_inputed):
        return 'Year not valid. Please do not enter older car than {}.'.format(year_inputed)
    
    def nr_seats(self):
        return "Please enter from 2 to 14 seats."
    
    def vehicle_type(self):
        return "Please enter either Sedan, Bus, Off Road or Small Car."