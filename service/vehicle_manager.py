from repos.vehicle_repo import VehicleRepo
from models.vehicle import Vehicle
import string
import time
import datetime


class VehicleManager:

    def __init__(self):
        self.__vehicle_repo = VehicleRepo()
        self.__temp_car_type = ""
        self.__temp_make = ""
        self.__temp_model = ""
        self.__temp_year = ""
        self.__temp_number_of_seats = ""
        self.__temp_license_plate = ""
        self.__temp_fuel = ""
        self.__temp_driving_transmission = ""

    def get_vehicle_list(self):
        return self.__vehicle_repo.get_vehicle_list()

    def save_new_car(self):
        # uses the temp values to save the new car 
        self.__vehicle_repo.save_new_car(
            self.__temp_license_plate,
            self.__temp_make,
            self.__temp_model,
            self.__temp_year,
            self.__temp_car_type,
            self.__temp_number_of_seats,
            self.__temp_fuel,
            self.__temp_driving_transmission)

    def check_type(self, car_type, ignore_empty_value=False, current_value=''):
        """Check if type is valid. Returns an error message if type
        has numbers or punctuation in it"""
        if car_type.strip() == '' and not ignore_empty_value:
            return self.error('Car type')
        elif car_type.strip() == '':
            self.__temp_car_type = current_value
            return None
        car_types = ["sedan", "offroad", "smallcar", "bus"]

        if car_type.strip() == '':
            return self.error("Car type")
        
        car_type = car_type.lower().replace(' ', '')
        if car_type.strip() in car_types:
            self.__temp_car_type = car_type
        else:
            return self.error("Car type")

    def check_make(self, make, ignore_empty_value=False, current_value=''):
        """Check if make is valid. Returns an error message if make
        has numbers or punctuation in it"""
        if make.strip() == '' and not ignore_empty_value:
            return self.error('Make')
        elif make.strip() == '':
            self.__temp_make = current_value
            return None

        if make.strip() == '':
            return self.error("Make")

        for letter in make.strip():
            if letter in (string.digits + string.punctuation):
                return self.error('Make')
        self.__temp_make = make

    def check_model(self, model, ignore_empty_value=False, current_value=''):
        """Checks if model is valid. Returns an error if it has punctuation in it"""
        if model.strip() == '' and not ignore_empty_value:
            return self.error('Model')
        elif model.strip() == '':
            self.__temp_make = current_value
            return None

        if model.strip() == '':
            return self.error("Model")
        for letter in model.strip():
            if letter in string.punctuation:
                return self.error('Model')
        self.__temp_model = model

    def check_year(self, year, ignore_empty_value=False, current_value=''):
        """Check if year is valid. Returns an error message if not"""
        if year.strip() == '' and not ignore_empty_value:
            return self.error('Year')
        elif year.strip() == '':
            self.__temp_year = current_value
            return None
        OLDEST_CAR = int(1940)
        present_year = int(datetime.datetime.today().year)
        
        if year.strip() == '':
            return self.error("Year")
        
        try:
            year = int(year.strip())
            if year > present_year or year < OLDEST_CAR:
                raise ValueError
        except ValueError:
            return self.error("Year")

        self.__temp_year = year

    def check_number_of_seats(self, number_of_seats, ignore_empty_value=False, current_value=''):
        """Check if number of seats is between 2 and 14. Returns an error message if not"""
        if number_of_seats.strip() == '' and not ignore_empty_value:
            return self.error('Number of seats')
        elif number_of_seats.strip() == '':
            self.__temp_number_of_seats = current_value
            return None
        if number_of_seats.strip() == '':
            return self.error("Number of seats")

        try:
            number_of_seats = int(number_of_seats.strip())
            if number_of_seats < 2 or number_of_seats > 14:
                raise ValueError
        except ValueError:
            return self.error("Number of seats")

        self.__temp_number_of_seats = number_of_seats

    def check_license_plate(self, license_plate, ignore_empty_value=False, current_value=''):
        """Check if license plate is valid. Returns an error message if number plate
        has punctuation in it"""
        if license_plate.strip() == '' and not ignore_empty_value:
            return self.error('License plate')
        elif license_plate.strip() == '':
            self.__temp_license_plate = current_value
            return None

        if license_plate.strip() == '' and not ignore_empty_value:
            return self.error("License plate")

        if len(license_plate) < 5 or len(license_plate) > 6:
            return self.error('License plate')
        
        for letter in license_plate:
            if letter in (string.punctuation):
                return self.error('License plate')
        self.__temp_license_plate = license_plate

    def check_fuel(self, fuel, ignore_empty_value=False, current_value=''):
        """Checks that input fuel is valid. Returns an error if it is not
        in our list of fuels"""
        if fuel.strip() == '' and not ignore_empty_value:
            return self.error('Fuel')
        elif fuel.strip() == '':
            self.__temp_fuel = current_value
            return None
        fuels = ["gasoline", "diesel", "electric", "hybrid"]

        if fuel.strip() == '':
            return self.error("Fuel")
        else:
            if fuel.lower().strip() in fuels:
                self.__temp_fuel = fuel
            else:
                return self.error("Fuel")

    def check_driving_transmission(self, driving_transmission, ignore_empty_value=False, current_value=''):
        """
        Driving transmission allowed: Automatic, Manual, 
        we don't have any other high tech crappy something.
        """
        if driving_transmission.strip() == '' and not ignore_empty_value:
            return self.error('Driving transmission')
        elif driving_transmission.strip() == '':
            self.__temp_driving_transmission = current_value
            return None
        transmissions = ["automatic", "manual"]

        if driving_transmission.strip() == '':
            return self.error("Driving transmission")
        else:
            if driving_transmission.lower().strip() in transmissions:
                self.__temp_driving_transmission = driving_transmission
            else:
                return self.error("Driving transmission")

    def find_car_by_license_plate(self, license_plate):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        for vehicle in cars_list:
            car_licence = vehicle.get_license().lower()
            if car_licence == license_plate.lower():
                return vehicle

    def find_car_by_make(self, make):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        cars = []
        for vehicle in cars_list:
            car_make = vehicle.get_make().lower()
            if car_make == make.lower():
                cars.append(vehicle)
        if cars != []:
            return cars

    def find_car_by_type(self, type_of_car, cars_list=''):
        #if cars_list == '':
        cars_list = self.__vehicle_repo.get_vehicle_list()
        cars = []
        for vehicle in cars_list:
            car_type = vehicle.get_vehicle_type().lower()
            if car_type == type_of_car.lower():
                cars.append(vehicle)
        if cars != []:
            return cars

    def show_car_availability(self, start_date, end_date, prompt):
        vehicles = self.get_vehicle_list()
        available_cars = []
        rented_cars = []

        dates = set()
        working_date = start_date
        one_day = datetime.timedelta(days=1)
        while working_date <= end_date:
            dates.add(working_date)
            working_date += one_day
        
        for car in vehicles:
            car_dates = set(car.get_rented_dates())
            check = car_dates & dates
            if len(check) == 0:
                available_cars.append(car)
            else:
                rented_cars.append(car)

        if prompt == 'available':
            return available_cars
        else:
            return rented_cars

    def save_order_dates(self, dates, license_plate):
        vehicle = self.find_car_by_license_plate(license_plate)
        self.__vehicle_repo.delete_vehicle(vehicle)
        a, b, c, d, e, f, g, h = vehicle.get_attributes()
        vehicle_dates = vehicle.get_rented_dates()

        vehicle_dates.extend(dates)
        new_dates = self.dates_to_string(vehicle_dates)
        
        self.__vehicle_repo.save_new_car(a, b, c, d, e, f, g, h, dates_rented=new_dates)

    def delete_order_dates(self, dates, license_plate):
        vehicle = self.find_car_by_license_plate(license_plate)
        a, b, c, d, e, f, g, h = vehicle.get_attributes()
        vehicle_dates = set(vehicle.get_rented_dates())
        self.__vehicle_repo.delete_vehicle(vehicle)
        new_dates = vehicle_dates - set(dates)
        new_vehicle_dates = self.dates_to_string(new_dates)
        self.__vehicle_repo.save_new_car(a, b, c, d, e, f, g, h, dates_rented=new_vehicle_dates)

    def dates_to_string(self, dates):
        new_dates = ''
        for v_day in dates:
            new_dates += str(v_day.year)
            if v_day.month <10:
                new_dates += '0' + str(v_day.month) 
            else:
                new_dates += str(v_day.month)
            if v_day.day < 10:
                new_dates += '0' + str(v_day.day) + ','
            else:
                new_dates += str(v_day.day) + ','
        return new_dates

    def delete_vehicle(self, car):
        self.__vehicle_repo.delete_vehicle(car)

    def error(self, input_type):
        return '{} not valid. Please try again.'.format(input_type)
