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
        self.__temp_number_plate = ""
        self.__temp_fuel = ""
        self.__temp_driving_transmission = ""

    def get_vehicle_list(self):
        return self.__vehicle_repo.get_vehicle_list()

    def save_new_car(self):
        # uses the temp values to save the new car 
        self.__vehicle_repo.save_new_car(
            self.__temp_number_plate,
            self.__temp_make,
            self.__temp_model,
            self.__temp_year,
            self.__temp_car_type,
            self.__temp_number_of_seats,
            self.__temp_fuel,
            self.__temp_driving_transmission)

    def check_type(self, car_type, ignore_empty_value=False, current_value=''):
        car_types = ["sedan", "offroad", "smallcar", "bus"]
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

    def check_make(self, make, ignore_empty_value=False, current_value=''):
        """Check if make is valid. Returns an error message if make
        has numbers or punctuation in it"""
        # TODO list of valid makes
        """
        This and the the model are going to be a pain, because a car
        can have several models, like toyota can have, yaris, auris, corolla,
        land cruiser, hilux, aygo, rav4 etc. 
        and audi can have, a3, a4, a6, a8, q7, q5 etc etc. 
        So maybe we should use dictionaries to store as makes as keys and 
        models as values.
        """
        if make.strip() == '':
            return self.error("Make")

        for letter in make.strip():
            if letter in (string.digits + string.punctuation):
                return self.error('Make')
        self.__temp_make = make

    def check_model(self, model, ignore_empty_value=False, current_value=''):
        # TODO list of valid models
        if model.strip() == '':
            return self.error("Model")
        self.__temp_model = model

    def check_year(self, year, ignore_empty_value=False, current_value=''):
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

    def check_number_of_seats(self, number_of_seats, ignore_empty_value=False, current_value=''):
        """Check if number of seats is valid. Returns an error message if number of seats
        has letters or punctuation in it"""
        """ I constrained the number of seats from 2-14
         as for 2 seater as the smallest car that you can rent,
         up to 14 seats as a small bus.
        """
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
        else:
            self.__temp_number_of_seats = number_of_seats

    def check_number_plate(self, number_plate, ignore_empty_value=False, current_value=''):
        """Check if number plate is valid. Returns an error message if number plate
        has punctuation in it"""

        if number_plate.strip() == '':
            return self.error("Number plate")

        for letter in number_plate:
            if letter in (string.punctuation):
                return self.error('Number of seats')
        self.__temp_number_plate = number_plate

    def check_fuel(self, fuel, ignore_empty_value=False, current_value=''):
        """
        Fuel can either be: bensin, diesel, electric and hybrid.
        """
        fuels = ["bensin", "diesel", "electric", "hybrid"]
        fuel_type = ""
        if fuel.strip() == '':
            return self.error("Fuel")
        else:
            for letter in fuel:
                if letter.isalpha():
                    fuel_type += letter.lower()
                else:
                    return self.error("Fuel")
        if fuel_type in fuels:
            self.__temp_fuel = fuel
        else:
            return self.fuels_allowed()

    def check_driving_transmission(self, driving_transmission, ignore_empty_value=False, current_value=''):
        """
        Driving transmission allowed: Automatic, Manual, 
        we don't have any other high tech crappy something.
        """
        transmissions = ["automatic", "manual"]
        inputed_transmission = ""
        if driving_transmission.strip() == '':
            return self.error("Driving transmission")
        else:
            for letter in driving_transmission:
                if letter.isalpha():
                    inputed_transmission += letter.lower()
                else:
                    return self.error("Driving transmission")
        if inputed_transmission in transmissions:
            self.__temp_driving_transmission = driving_transmission
        else:
            return self.transmission_allowed()

    def find_car_by_number_plate(self, number_plate):
        cars_list = self.__vehicle_repo.get_vehicle_list()
        for vehicle in cars_list:
            car_licence = vehicle.get_licence().lower()
            if car_licence == number_plate.lower():
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
        if cars_list == '':
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

    def save_order_dates(self, dates, vehicle_number):
        vehicle = self.find_car_by_number_plate(vehicle_number)
        self.__vehicle_repo.delete_vehicle(vehicle)
        a, b, c, d, e, f, g, h, i = vehicle.get_attributes()
        vehicle_dates = vehicle.get_rented_dates()

        vehicle_dates.extend(dates)
        new_dates = self.dates_to_string(vehicle_dates)
        
        self.__vehicle_repo.save_new_car(a, b, c, d, e, f, g, h, i, dates_rented=new_dates)

    def delete_order_dates(self, dates, vehicle_number):
        vehicle = self.find_car_by_number_plate(vehicle_number)
        a, b, c, d, e, f, g, h, i = vehicle.get_attributes()
        vehicle_dates = set(vehicle.get_rented_dates())
        self.__vehicle_repo.delete_vehicle(vehicle)
        new_dates = vehicle_dates - set(dates)
        #[day for day in vehicle_dates not in dates]
        new_vehicle_dates = self.dates_to_string(new_dates)
        self.__vehicle_repo.save_new_car(a, b, c, d, e, f, g, h, i, dates_rented=new_vehicle_dates)

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

    def newer(self, year_inputed):
        return 'Year not valid. Please do not enter newer car than {}.'.format(year_inputed)

    def older(self, year_inputed):
        return 'Year not valid. Please do not enter older car than {}.'.format(year_inputed)

    def nr_seats(self):
        return "Please enter from 2 to 14 seats."

    def vehicle_type(self):
        return "Please enter either Sedan, Bus, Off Road or Small Car."

    def fuels_allowed(self):
        return "Fuel can be: Bensin, Diesel, Electric or Hybrid."

    def transmission_allowed(self):
        return "Please enter either Automatic or Manual transmissions."
