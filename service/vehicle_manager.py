from repos.vehicle_repo import VehicleRepo
from models.vehicle import Vehicle
import string
import time
import datetime


class VehicleManager:

    def __init__(self):
        self.__vehicle_repo = VehicleRepo()
        self.__temp_vehicle_type = ""
        self.__temp_make = ""
        self.__temp_model = ""
        self.__temp_year = ""
        self.__temp_number_of_seats = ""
        self.__temp_license_plate = ""
        self.__temp_fuel = ""
        self.__temp_driving_transmission = ""

    def get_vehicle_list(self):
        return self.__vehicle_repo.get_vehicle_list()
    
    def get_license(self):
        return self.__temp_license_plate

    def save_new_vehicle(self):
        """uses the temp values to save the new vehicle""" 
        self.__vehicle_repo.save_new_vehicle(
            self.__temp_license_plate,
            self.__temp_make,
            self.__temp_model,
            self.__temp_year,
            self.__temp_vehicle_type,
            self.__temp_number_of_seats,
            self.__temp_fuel,
            self.__temp_driving_transmission
        )

    def check_type(self, vehicle_type, ignore_empty_value=False, current_value=""):
        """Check if type is valid. Returns an error message if type
        does not match our list of types. When editing a previous value 
        is used if nothing is entered.
        """
        if vehicle_type.strip() == "" and not ignore_empty_value:
            return self.error("Vehicle type")
        elif vehicle_type.strip() == "":
            self.__temp_vehicle_type = current_value
            return None
        vehicle_types = ["sedan", "offroad", "smallcar", "bus"]

        if vehicle_type.strip() == "":
            return self.error("Vehicle type")
        
        vehicle_type = vehicle_type.lower().replace(" ", "")
        if vehicle_type.strip() in vehicle_types:
            self.__temp_vehicle_type = vehicle_type
        else:
            return self.error("Vehicle type")

    def check_make(self, make, ignore_empty_value=False, current_value=""):
        """Check if make is valid. Returns an error message if make
        has numbers or punctuation in it. When editing a previous
        value is used if nothing is entered.
        """
        if make.strip() == "" and not ignore_empty_value:
            return self.error("Make")
        elif make.strip() == "":
            self.__temp_make = current_value
            return None

        if make.strip() == "":
            return self.error("Make")
        for letter in make.strip():
            if letter in (string.digits + string.punctuation):
                return self.error("Make")
        self.__temp_make = make

    def check_model(self, model, ignore_empty_value=False, current_value=""):
        """Checks if model is valid. Returns an error if it has 
        punctuation in it. When editing a previous value is used
        if nothing is entered.
        """
        if model.strip() == "" and not ignore_empty_value:
            return self.error("Model")
        elif model.strip() == "":
            self.__temp_model = current_value
            return None

        if model.strip() == "":
            return self.error("Model")
        for letter in model.strip():
            if letter in string.punctuation:
                return self.error("Model")
        self.__temp_model = model

    def check_year(self, year, ignore_empty_value=False, current_value=""):
        """Check if year is valid. Returns an error message if it is not
        between 1940 and the current year. When editing a previous 
        value is used if nothing is entered.
        """
        OLDEST_VEHICLE = int(1940)
        present_year = int(datetime.datetime.today().year)        
        
        if year.strip() == "" and not ignore_empty_value:
            return self.error("Year")
        elif year.strip() == "":
            self.__temp_year = current_value
            return None
        if year.strip() == "":
            return self.error("Year")
        
        try:
            year = int(year.strip())
            if year > present_year or year < OLDEST_VEHICLE:
                raise ValueError
        except ValueError:
            return self.error("Year")
        self.__temp_year = year

    def check_number_of_seats(self, seats, ignore_empty_value=False, current_value=""):
        """Check if number of seats is between 2 and 14. Returns an error 
        message if not. When editing a previous value is used if 
        nothing is entered.
        """
        if seats.strip() == "" and not ignore_empty_value:
            return self.error("Number of seats")
        elif seats.strip() == "":
            self.__temp_number_of_seats = current_value
            return None
        
        if seats.strip() == "":
            return self.error("Number of seats")

        try:
            seats = int(seats.strip())
            if seats < 2 or seats > 14:
                raise ValueError
        except ValueError:
            return self.error("Number of seats")
        self.__temp_number_of_seats = seats

    def check_license_plate(self, license_plate, ignore_empty_value=False, current_value=""):
        """Check if license plate is valid. Returns an error message if number 
        plate has punctuation in it. When editing a previous value is 
        used if nothing is entered.
        """
        license_plate = license_plate.replace(" ", "")
        
        if license_plate.strip() == "" and not ignore_empty_value:
            return self.error("License plate")
        elif license_plate.strip() == "":
            self.__temp_license_plate = current_value
            return None

        if len(license_plate) < 3 or len(license_plate) > 6:
            return self.error("License plate")
        
        for letter in license_plate:
            if letter in (string.punctuation):
                return self.error("License plate")
        self.__temp_license_plate = license_plate

    def check_fuel(self, fuel, ignore_empty_value=False, current_value=""):
        """Checks that input fuel is valid. Returns an error if it is not
        in our list of fuels. When editing a previous value is used 
        if nothing is entered.
        """
        fuels = ["gasoline", "diesel", "electric", "hybrid"]
        
        if fuel.strip() == "" and not ignore_empty_value:
            return self.error("Fuel")
        elif fuel.strip() == "":
            self.__temp_fuel = current_value
            return None

        if fuel.strip() == "":
            return self.error("Fuel")
        else:
            if fuel.lower().strip() in fuels:
                self.__temp_fuel = fuel
            else:
                return self.error("Fuel")

    def check_driving_transmission(
            self, driving_transmission, ignore_empty_value=False, current_value=""):
        """Checks that input driving transmission is valid. Returns an 
        error if it is not in our list of fuels. When editing a 
        previous value is used if nothing is entered.
        """
        transmissions = ["automatic", "manual"]        
        
        if driving_transmission.strip() == "" and not ignore_empty_value:
            return self.error("Driving transmission")
        elif driving_transmission.strip() == "":
            self.__temp_driving_transmission = current_value
            return None

        if driving_transmission.strip() == "":
            return self.error("Driving transmission")
        else:
            if driving_transmission.lower().strip() in transmissions:
                self.__temp_driving_transmission = driving_transmission
            else:
                return self.error("Driving transmission")

    def find_vehicle_by_license_plate(self, license_plate):
        """Searches through a list of vehicles to find one whose license 
        plate matches the given license. Returns a matched vehicle 
        instance or None if no vehicle is found.
        """
        license_plate = license_plate.replace(" ", "")

        vehicle_list = self.__vehicle_repo.get_vehicle_list()
        for vehicle in vehicle_list:
            vehicle_license = vehicle.get_license().lower()
            if vehicle_license == license_plate.lower():
                return vehicle

    def find_vehicle_by_make(self, make):
        """Searches through a list of vehicles to find those whose make 
        matches the given make. Returns a list of matched vehicles 
        or None if no vehicles are found.
        """
        vehicle_list = self.__vehicle_repo.get_vehicle_list()
        vehicles = []
        for vehicle in vehicle_list:
            vehicle_make = vehicle.get_make().lower()
            if vehicle_make == make.lower():
                vehicles.append(vehicle)
        if vehicles != []:
            return vehicles

    def find_vehicle_by_type(self, type_of_vehicle, vehicle_list=""):
        """Searches through a list of vehicles to find those whose type 
        matches the given type. Returns a list of matched vehicles 
        or None if no vehicles are found.
        """
        type_of_vehicle = type_of_vehicle.replace(" ", "")
        # if no car list is given go to vehicle_repo to get one
        if vehicle_list == "":
            vehicle_list = self.__vehicle_repo.get_vehicle_list()
        vehicles = []
        for vehicle in vehicle_list:
            vehicle_type = vehicle.get_vehicle_type().lower()
            if vehicle_type == type_of_vehicle.lower():
                vehicles.append(vehicle)
        if vehicles != []:
            return vehicles

    def show_vehicle_availability(self, start_date, end_date, prompt):
        """Goes through a list of vehicles and splits them into two 
        lists based on whether they are available or rented on the 
        given dates. Returns a list based on the prompt given.
        """
        vehicles = self.get_vehicle_list()
        available_vehicles = []
        rented_vehicles = []

        dates = set()
        # adds start and end dates and every day between them to a set of dates
        working_date = start_date
        one_day = datetime.timedelta(days=1)
        while working_date <= end_date:
            dates.add(working_date)
            working_date += one_day
        
        for vehicle in vehicles:
            # get dates from each car and creates a set to compare with the entered dates
            vehicle_dates = set(vehicle.get_rented_dates())
            check = vehicle_dates & dates
            if len(check) == 0:
                available_vehicles.append(vehicle)
            else:
                rented_vehicles.append(vehicle)

        if prompt == "available":
            return available_vehicles
        else:
            return rented_vehicles

    def save_order_dates(self, dates, license_plate):
        """Finds a vehicle based on license plate, deletes it from file, 
        adds dates to its dates_rented attribute and saves it again.
        """
        vehicle = self.find_vehicle_by_license_plate(license_plate)
        
        # Getting everything needed to recreate the Vehicle instance
        a, b, c, d, e, f, g, h = vehicle.get_attributes()
        vehicle_dates = vehicle.get_rented_dates()
        self.__vehicle_repo.delete_vehicle(vehicle)

        # Adding the new dates and saving them as strings
        vehicle_dates.extend(dates)
        new_dates = self.dates_to_string(vehicle_dates)
        
        self.__vehicle_repo.save_new_vehicle(a, b, c, d, e, f, g, h, dates_rented=new_dates)

    def delete_order_dates(self, dates, license_plate):
        """Finds a vehicle based on license plate, deletes it from file, 
        removes dates to its dates_rented attribute and saves it again.
        """
        vehicle = self.find_vehicle_by_license_plate(license_plate)

        # Getting everything needed to recreate the Vehicle instance        
        a, b, c, d, e, f, g, h = vehicle.get_attributes()
        vehicle_dates = set(vehicle.get_rented_dates())
        self.__vehicle_repo.delete_vehicle(vehicle)
        
        # Removing dates and converting what"s left to strings
        new_dates = vehicle_dates - set(dates)
        new_vehicle_dates = self.dates_to_string(new_dates)
        self.__vehicle_repo.save_new_vehicle(
            a, b, c, d, e, f, g, h, dates_rented=new_vehicle_dates)

    def dates_to_string(self, dates):
        """Recieves a list of dates and converts them into a single string
        of information, where every date has 8 numbers in it.
        """
        new_dates = ""
        for v_day in dates:
            new_dates += str(v_day.year)
            if v_day.month <10:
                new_dates += "0" + str(v_day.month) 
            else:
                new_dates += str(v_day.month)
            if v_day.day < 10:
                new_dates += "0" + str(v_day.day) + ","
            else:
                new_dates += str(v_day.day) + ","
        return new_dates

    def delete_vehicle(self, vehicle):
        self.__vehicle_repo.delete_vehicle(vehicle)

    def error(self, input_type):
        """An error message used by all check methods"""
        return "{} not valid. Please try again.".format(input_type)
