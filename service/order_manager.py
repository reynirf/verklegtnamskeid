from repos.order_repo import OrderRepo
from models.order import Order
from models.vehicle import Vehicle
from datetime import timedelta
from datetime import date
from service.vehicle_manager import VehicleManager
import time
import string


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
        self.__locations = ["reykjavik", "akureyri", 'ak', 'rvk']
    
    def get_order_list(self):
        return self.__order_repo.get_order_list()

    def get_dates(self):
        return self.__temp_start_date, self.__temp_end_date

    def get_type(self):
        return self.__temp_type_of_vehicle

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
            self.__temp_type_of_vehicle)

    def dates_to_string(self, dates):
        new_dates = str(dates.year)
        if dates.month <10:
            new_dates += '0' + str(dates.month) 
        else:
            new_dates += str(dates.month)
        if dates.day < 10:
            new_dates += '0' + str(dates.day)
        else:
            new_dates += str(dates.day)
        return new_dates

    def get_inputted_order(self):
        print("Enter ID: {}".format(self.__temp_ID))
        print("Enter SSN: {}".format(self.__temp_ssn))
        print("Enter start date: {}".format(self.__temp_start_date))
        print("Enter ending date: {}".format(self.__temp_end_date))
        print("Enter pick up time (24H): {}".format(self.__temp_pick_up_time))
        print("Enter returning time (24H): {}".format(self.__temp_returning_time))
        print("Enter pick up location: {}".format(self.__temp_pick_up_location))
        print("Enter return location: {}".format(self.__temp_return_location))
        print("Enter type of vehicle: {}".format(self.__temp_type_of_vehicle))
        start_date, end_date = self.get_dates()
        car_list = self.__vehicle_manager.show_car_availability(start_date, end_date, 'available')
        car_type = self.get_type()
        filtered_list = self.__vehicle_manager.find_car_by_type(car_type, car_list)
        print()
        print('Available cars:')
        print()
        print('{:<20} {:<20} {:<20} {:<20}'.format('License', 'Make', 'Model', 'Seats'))
        print('-'*70)
        for car in filtered_list:
            print(car.availability_string())
        print()
        print("Enter license plate: {}".format(self.__temp_license_plate))
        print("Enter Insurance: {}".format(self.__temp_insurance))
        print()
        return filtered_list
        

    def get_order_dates(self, start='', end=''):
        if start == '':
            start = self.__temp_start_date
        if end == '':
            end = self.__temp_end_date
        
        dates = []
        working_date = start
        one_day = timedelta(days=1)
        while working_date <= end:
            dates.append(working_date)
            working_date += one_day
        return dates 

    def get_license_plate(self):
        return self.__temp_license_plate

    def calculate_order(self):
        start_date_Input = self.__temp_start_date
        end_date_Input = self.__temp_end_date
        extra_insurance = self.__temp_insurance

        order_instance=Vehicle(0,0,0,0,self.__temp_type_of_vehicle,0,0,0)
        price_per_day = order_instance.get_price_per_day()

        if extra_insurance.lower() == 'yes':
            extra_insurance_per_day = order_instance.get_insurance_per_day()
        else:
            extra_insurance_per_day = 0

        diffrence = end_date_Input - start_date_Input
        total_days = diffrence.days + 1
        basic_insurance_cost = int(price_per_day * 0.35)
        return price_per_day, basic_insurance_cost, extra_insurance_per_day, total_days

    def check_ID(self, ID, ignore_empty_value=False, current_value=''):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""
        if self.find_order_by_id(ID):
            return 'An order with that ID already exists. Choose another ID'
        if ID.strip() == '' and not ignore_empty_value: #and not ignore_empty_value:
            return self.error('ID')
        elif ID.strip() == '':
            self.__temp_ID = current_value
            return None

        if len(ID) > 8:
            return self.error('ID')
        for letter in ID:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error('ID')
        self.__temp_ID = ID

    def check_ssn(self, ssn, ignore_empty_value=False, current_value=''):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""
        if ssn.strip() == '' and not ignore_empty_value:
            return self.error('SSN')
        elif ssn.strip() == '':
            self.__temp_ssn = current_value
            return None
        
        ssn = ssn.replace("-", "")
        if len(ssn) < 8 or len(ssn) > 12:
            return self.error('SSN')
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error('SSN')
        self.__temp_ssn = ssn

    def check_type_of_vehicle(self, type_of_vehicle, ignore_empty_value=False, current_value=''):
        """check if type of car is valid."""
        if type_of_vehicle.strip() == '' and not ignore_empty_value:
            return self.error( 'Type' )
        elif type_of_vehicle.strip() == '':
            self.__temp_type_of_vehicle = current_value
            return None
        
        car_types = ["sedan", "offroad", "smallcar", "bus"]
        
        type_of_vehicle = type_of_vehicle.replace(' ', '')
        if type_of_vehicle.lower() in car_types:
            self.__temp_type_of_vehicle = type_of_vehicle
        else:
            return self.error("Car type")

    def create_start_date_object(self, date_str):
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
            return self.error('Start date')

    def create_end_date_object(self, date_str):
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

    def check_start_date(self, start_date, ignore_empty_value=False, current_value=''):
        """Check if start date is valid. Returns an error message if start date
        can not be converted to a datetime object"""
        if start_date.strip() == '' and not ignore_empty_value:
            return self.error('Start date')
        elif start_date.strip() == '':
            self.__temp_start_date = self.create_start_date_object(current_value)
            return None
        self.__temp_start_date = self.create_start_date_object(start_date)
        if not self.__temp_start_date:
            return self.error('Start date')

    def check_ending_date(self, end_date, ignore_empty_value=False, current_value=''):
        """Check if end date is valid. Returns an error message if end date
        can not be converted to a datetime object"""
        if end_date.strip() == '' and not ignore_empty_value:
            return self.error('End date')
        elif end_date.strip() == '':
            self.__temp_end_date = self.create_end_date_object(current_value)
            return None
        self.__temp_end_date = self.create_end_date_object(end_date)
        if not self.__temp_end_date:
            return self.error('End date')

    def check_pick_up_time(self, pick_up_time, ignore_empty_value=False, current_value=''):
        """Check if pick up time is valid. Returns an error message if pick up time
        has letters in it"""
        #slice_list=list(pick_up_time)
        if pick_up_time.strip() == '' and not ignore_empty_value:
            try:
                check_time = time.strptime(pick_up_time,"%H:%M")
            except ValueError:
                return self.error('Pick up time')
        elif pick_up_time.strip() == '':
            self.__temp_pick_up_time = current_value
            return None
        else:
            self.__temp_pick_up_time = pick_up_time

    def check_returning_time(self, returning_time, ignore_empty_value=False, current_value=''):
        """Check if returning time is valid. Returns an error message if returning time
        has letters in it"""
        if returning_time.strip() == '' and not ignore_empty_value:
            try:
                check_time = time.strptime(returning_time,"%H:%M")
            except ValueError:
                return self.error('Return time')
        elif returning_time.strip() == '':
            self.__temp_returning_time = current_value
            return None
        else:
            self.__temp_returning_time = returning_time


    def check_pick_up_location(self, pick_up_location, ignore_empty_value=False, current_value=''):
        """Check if location matches our list of locations"""
        if pick_up_location.strip() == '' and not ignore_empty_value:
            return self.error('Pick up location')
        elif pick_up_location.strip() == '':
            self.__temp_pick_up_location = current_value
            return None
        
        if pick_up_location.lower().strip() in self.__locations:
            self.__temp_pick_up_location = pick_up_location
        else:
            return self.error('Pick up location')

    def check_return_location(self, return_location, ignore_empty_value=False, current_value=''):
        """Check if location matches our list of locations"""
        if return_location.strip() == '' and not ignore_empty_value:
            return self.error('Return location')
        elif return_location.strip() == '':
            self.__temp_return_location = current_value
            return None
        if return_location.lower().strip() in self.__locations:
            self.__temp_return_location = return_location
        else:
            return self.error('Pick up location')

    def check_license_plate(self, license_plate, ignore_empty_value=False, current_value=''):
        """Check if license plate is valid. Returns an error message if license plate
        has punctuation in it"""
        if license_plate.strip() == '' and not ignore_empty_value:
            return self.error('License plate')
        elif license_plate.strip() == '' and current_value:
            self.__temp_license_plate = current_value
            return None
        # TODO this should accept also entering the license number in lowercase.
        if len(license_plate) != 5:
            return self.error('License plate')
        
        for letter in license_plate:
            if letter in (string.punctuation):
                return self.error('License plate')
        if license_plate not in ignore_empty_value:
            return 'License plate does not exist. Find a plate in the list above and try again.'
        self.__temp_license_plate = license_plate

    def check_insurance(self, insurance, ignore_empty_value=False, current_value=''):
        if insurance.strip() == '' and not ignore_empty_value:
            return self.error('Insurance')
        elif insurance.strip() == '':
            self.__temp_insurance = current_value
            return None
        insurance = insurance.strip()
        if insurance.lower() == "yes" or insurance.lower() == "no" or insurance.lower() == 'n' or insurance.lower() == 'y':
            self.__temp_insurance = insurance
        else:
            return self.error('Insurance')

    def find_order_by_ssn(self, ssn):
        order_list = self.__order_repo.get_order_list()
        ssn = ssn.replace("-", "")
        orders = []
        for order in order_list:
            order_ssn = order.get_ssn().replace("-", "")
            if order_ssn == ssn:
                orders.append(order)
        return orders

    def find_order_by_id(self, ID):
        order_list = self.__order_repo.get_order_list()
        for order in order_list:
            if order.get_id() == ID:
                return order
    
    def find_orders_by_vehicle(self, license_plate):
        order_list = self.__order_repo.get_order_list()
        orders = []
        for order in order_list:
            vehicle = order.get_license_plate()
            if vehicle.lower() == license_plate.lower():
                orders.append(order)
        return orders

    def find_orders_by_vehicle(self, license_plate):
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
        return '{} not valid. Please try again.'.format(input_type)
