from repos.order_repo import OrderRepo
from models.order import Order
from models.vehicle import Vehicle
from datetime import timedelta
from datetime import date
from service.vehicle_manager import VehicleManager
import time
import string
import datetime


class OrderManager:
    
    def __init__(self):
        self.__order_repo = OrderRepo()
        self.__vehicle_manager = VehicleManager()
        self.__temp_id = ""
        self.__temp_customer = ""
        self.__temp_start_date = ""
        self.__temp_end_date = ""
        self.__temp_pick_up_time = ""
        self.__temp_returning_time = ""
        self.__temp_pick_up_location = ""
        self.__temp_return_location = ""
        self.__temp_licese_plate = ""
        self.__temp_insurance = ""
        self.__temp_type_of_vehicle = ""
        self.__locations = ["reykjavik", "akureyri", "ak", "rvk"]
    
    def get_order_list(self):
        return self.__order_repo.get_order_list()

    def get_dates(self):
        return self.__temp_start_date, self.__temp_end_date

    def get_type(self):
        return self.__temp_type_of_vehicle
    
    def get_license_plate(self):
        return self.__temp_license_plate
    
    def save_new_order(self):
        """uses the temp values to save the new customer"""
        start_day = self.dates_to_string(self.__temp_start_date)
        end_day = self.dates_to_string(self.__temp_end_date)
        self.__order_repo.save_new_order(
            self.__temp_ID,
            self.__temp_ssn,
            start_day,
            end_day,
            self.__temp_pick_up_time,
            self.__temp_returning_time,
            self.__temp_pick_up_location,
            self.__temp_return_location,
            self.__temp_license_plate,
            self.__temp_insurance,
            self.__temp_type_of_vehicle
        )

    def dates_to_string(self, dates):
        """Recieves a date and converts it into a single string
        with 8 numbers in it"""
        new_dates = str(dates.year)
        if dates.month <10:
            new_dates += "0" + str(dates.month) 
        else:
            new_dates += str(dates.month)
        if dates.day < 10:
            new_dates += "0" + str(dates.day)
        else:
            new_dates += str(dates.day)
        return new_dates

    def get_inputted_order(self):
        """Prints the prompts and temp values needed when editing an order. Searches
        for available vehicles based on the input"""
        print("Enter ID: {}".format(self.__temp_ID))
        print("Enter SSN: {}".format(self.__temp_ssn))
        print("Enter start date: {}".format(self.__temp_start_date))
        print("Enter ending date: {}".format(self.__temp_end_date))
        print("Enter pick up time (24H): {}".format(self.__temp_pick_up_time))
        print("Enter returning time (24H): {}".format(self.__temp_returning_time))
        print("Enter pick up location: {}".format(self.__temp_pick_up_location))
        print("Enter return location: {}".format(self.__temp_return_location))
        print("Enter type of vehicle: {}".format(self.__temp_type_of_vehicle))
        print("Enter license plate: {}".format(self.__temp_license_plate))
        print("Enter Insurance: {}".format(self.__temp_insurance))
        print()
        
    def get_order_dates(self, start="", end=""):
        """Adds start and end dates and every day between them to a list of dates.
        If start and end values are empty temp values are used"""
        if start == "":
            start = self.__temp_start_date
        if end == "":
            end = self.__temp_end_date
        
        dates = []
        working_date = start
        one_day = timedelta(days=1)
        while working_date <= end:
            dates.append(working_date)
            working_date += one_day
        return dates 

    def calculate_order(self):
        """Uses the temp values to find the values needed to calculate the
        price of the order."""
        start_date_Input = self.__temp_start_date
        end_date_Input = self.__temp_end_date
        extra_insurance = self.__temp_insurance

        # Creating a Vehicle instance to get the prices
        order_instance=Vehicle(0,0,0,0,self.__temp_type_of_vehicle,0,0,0)
        price_per_day = order_instance.get_price_per_day()
        if extra_insurance.lower() == "yes":
            extra_insurance_per_day = order_instance.get_insurance_per_day()
        else:
            extra_insurance_per_day = 0

        # Calculating the number of days and basic insurance price
        diffrence = end_date_Input - start_date_Input
        total_days = diffrence.days + 1
        basic_insurance_cost = int(price_per_day * 0.35)
        return price_per_day, basic_insurance_cost, extra_insurance_per_day, total_days

    def check_ID(self, ID, ignore_empty_value=False, current_value=""):
        """Check if ID is valid. Returns an error message if ID is invalid
        or if it already exists. When editing a previous value is used 
        if nothing is entered"""
        if self.find_order_by_id(ID):
            return "An order with that ID already exists or the ID is invalid. Choose another ID"
        if ID.strip() == "" and not ignore_empty_value: #and not ignore_empty_value:
            return "An order with that ID already exists or the ID is invalid. Choose another ID"        
        elif ID.strip() == "":
            self.__temp_ID = current_value
            return None

        if len(ID) > 8:
            return "An order with that ID already exists or the ID is invalid. Choose another ID"
        for letter in ID:
            if letter in (string.ascii_letters + string.punctuation):
                return "An order with that ID already exists or the ID is invalid. Choose another ID"
        self.__temp_ID = ID

    def check_ssn(self, ssn, ignore_empty_value=False, current_value=""):
        """Check if ssn is valid. Returns an error message if ssn is invalid. 
        When editing a previous value is used if nothing is entered"""
        if ssn.strip() == "" and not ignore_empty_value:
            return self.error("SSN")
        elif ssn.strip() == "":
            self.__temp_ssn = current_value
            return None
        
        ssn = ssn.replace("-", "")
        if len(ssn) < 8 or len(ssn) > 12:
            return self.error("SSN")
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error("SSN")
        self.__temp_ssn = ssn

    def check_type_of_vehicle(
            self, type_of_vehicle, ignore_empty_value=False, current_value=""):
        """check if type of vehicle is valid. Returns an error message if type 
        does not match our list of vehicles. When editing a previous value is 
        used if nothing is entered"""
        if type_of_vehicle.strip() == "" and not ignore_empty_value:
            return self.error( "Type" )
        elif type_of_vehicle.strip() == "":
            self.__temp_type_of_vehicle = current_value
            return None
        
        vehicle_types = ["sedan", "offroad", "smallcar", "bus"]
        
        type_of_vehicle = type_of_vehicle.replace(" ", "")
        if type_of_vehicle.lower() in vehicle_types:
            self.__temp_type_of_vehicle = type_of_vehicle
        else:
            return self.error("Vehicle type")

    def create_start_date_object(self, date_str):
        """Creates a date object from a string and compares it to the current date.
        Returns an error if it is not possible to convert to a date or if it is
        a date in the past"""
        present_day = date.today()
        try:
            year = date_str[6:]
            month = date_str[3:5]
            day = date_str[:2]
            date_object = date(int(year), int(month), int(day))
            if date_object < present_day:
                raise ValueError
            return date_object
        except ValueError:
            return self.error("Start date")

    def create_end_date_object(self, date_str):
        """Creates a date object from a string and compares it to the temp start
        date. Returns an error if it is not possible to convert to a date or if
        it is a date that"s older than the start date"""
        try:
            year = date_str[6:]
            month = date_str[3:5]
            day = date_str[:2]
            date_object = date(int(year), int(month), int(day))
            if date_object < self.__temp_start_date:
                raise ValueError
            return date_object
        except ValueError:
            return None

    def check_start_date(self, start_date, ignore_empty_value=False, current_value=""):
        """Check if start date is valid. Returns an error message if not. When editing 
        a previous value is used if nothing is entered"""
        if start_date.strip() == "" and not ignore_empty_value:
            return self.error("Start date")         
        elif start_date.strip() == "":
            self.__temp_start_date = self.create_start_date_object(current_value)
            return None
        start_date_object = self.create_start_date_object(start_date)
        if type(start_date_object) == date:
            self.__temp_start_date = start_date_object
        else:
            return self.error("Start date")

    def check_ending_date(self, end_date, ignore_empty_value=False, current_value=""):
        """Check if end date is valid. Returns an error message if not. When editing 
        a previous value is used if nothing is entered"""
        if end_date.strip() == "" and not ignore_empty_value:
            return self.error("End date")
        elif end_date.strip() == "":
            self.__temp_end_date = self.create_end_date_object(current_value)
            return None

        end_date_object = self.create_end_date_object(end_date)
        if type(end_date_object) == date:
            self.__temp_end_date = end_date_object
        else:
            return self.error("End date")

    def check_pick_up_time(self, pick_up_time, ignore_empty_value=False, current_value=""):
        """Check if pick up time is valid. Returns an error message if pick up time
        can not be converted to a time object. When editing a previous value 
        is used if nothing is entered"""
        if pick_up_time.strip() == "" and not ignore_empty_value:
            try:
                time.strptime(pick_up_time,"%H:%M")
            except ValueError:
                return self.error("Pick up time")
        elif pick_up_time.strip() == "":
            self.__temp_pick_up_time = current_value
            return None
        else:
            try:
                # Trying to convert to a time object and then saving as a string
                time_tuple = time.strptime(pick_up_time,"%H:%M")
                hours = time_tuple[3]
                minutes = time_tuple[4]
                if minutes < 10:
                    minutes = "0" + str(minutes)
                self.__temp_pick_up_time = "{}:{}".format(hours, minutes)
            except ValueError:
                return self.error("Pick up time")

    def check_returning_time(self, returning_time, ignore_empty_value=False, current_value=""):
        """Check if returning time is valid. Returns an error message if returning 
        time can not be converted to a time object. When editing a previous value 
        is used if nothing is entered"""
        if returning_time.strip() == "" and not ignore_empty_value:
            try:
                time.strptime(returning_time,"%H:%M")
            except ValueError:
                return self.error("Return time")
        elif returning_time.strip() == "":
            self.__temp_returning_time = current_value
            return None
        else:
            try:
                # Trying to convert to a time object and then saving as a string
                time_tuple = time.strptime(returning_time,"%H:%M")
                hours = time_tuple[3]
                minutes = time_tuple[4]
                if minutes < 10:
                    minutes = "0" + str(minutes)
                self.__temp_returning_time = "{}:{}".format(hours, minutes)
            except ValueError:
                return self.error("Return time")


    def check_pick_up_location(self, pick_up_location, ignore_empty_value=False, current_value=""):
        """Check if location matches our list of locations. Returns an error if not.
        When editing a previous value is used if nothing is entered"""
        if pick_up_location.strip() == "" and not ignore_empty_value:
            return self.error("Pick up location")
        elif pick_up_location.strip() == "":
            self.__temp_pick_up_location = current_value
            return None
        
        if pick_up_location.lower().strip() in self.__locations:
            self.__temp_pick_up_location = pick_up_location
        else:
            return self.error("Pick up location")

    def check_return_location(self, return_location, ignore_empty_value=False, current_value=""):
        """Check if location matches our list of locations. Returns an error if not.
        When editing a previous value is used if nothing is entered"""
        if return_location.strip() == "" and not ignore_empty_value:
            return self.error("Return location")
        elif return_location.strip() == "":
            self.__temp_return_location = current_value
            return None
        
        if return_location.lower().strip() in self.__locations:
            self.__temp_return_location = return_location
        else:
            return self.error("Pick up location")

    def check_license_plate(self, license_plate, ignore_empty_value=False, current_value=""):
        """Check if license plate is valid. Returns an error message if not. 
        When editing a previous value is used if nothing is entered"""
        license_plate = license_plate.replace(" ", "")
        if license_plate.strip() == "" and not ignore_empty_value:
            return self.error("License plate")
        elif license_plate.strip() == "" and current_value:
            self.__temp_license_plate = current_value
            return None
        
        if 3 > len(license_plate) or len(license_plate) > 6:
            return self.error("License plate")
        for letter in license_plate:
            if letter in (string.punctuation):
                return self.error("License plate")
        if license_plate.lower() not in ignore_empty_value:
            return "License plate does not exist. Find a plate in the list above and try again."
        self.__temp_license_plate = license_plate

    def check_insurance(self, insurance, ignore_empty_value=False, current_value=""):
        """Check that a valid answer has been given for insurance. Returns an error
        message if not. When editing a previous value is used if nothing is entered"""
        valid_answers = ["yes", "no", "y", "n"]
        insurance = insurance.strip()
        
        if insurance == "" and not ignore_empty_value:
            return self.error("Insurance")
        elif insurance == "":
            self.__temp_insurance = current_value
            return None
        
        if insurance.lower() in valid_answers:
            self.__temp_insurance = insurance
        else:
            return self.error("Insurance")

    def find_order_by_ssn(self, ssn):
        """Searches through a list of orders to find those whose SSN matches the
        SSN given. Returns a list of orders or None if no orders are found"""
        order_list = self.__order_repo.get_order_list()
        ssn = ssn.replace("-", "")
        orders = []
        for order in order_list:
            order_ssn = order.get_ssn().replace("-", "")
            if order_ssn == ssn:
                orders.append(order)
        return orders

    def find_order_by_id(self, ID):
        """Searches through a list of orders to find one whose ID matches the 
        one given. Returns an order or None if no order matches the ID"""
        order_list = self.__order_repo.get_order_list()
        for order in order_list:
            if order.get_id() == ID:
                return order

    def find_orders_by_vehicle(self, license_plate):
        """Searches through a list of orders to find those with the given vehicle
        license plate. Returns a list of orders or None if no orders are found"""
        order_list = self.__order_repo.get_order_list()
        orders = []
        for order in order_list:
            vehicle = order.get_license_plate()
            if vehicle.lower() == license_plate.lower():
                orders.append(order)
        return orders

    def delete_order(self, order):
        self.__order_repo.delete_order(order)
    
    def error(self, input_type):
        """An error message used by all check methods"""
        return "{} not valid. Please try again.".format(input_type)
