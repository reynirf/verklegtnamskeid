from repos.order_repo import OrderRepo
from models.order import Order
import string
from models.vehicle import Vehicle
from datetime import timedelta
from datetime import date
import time


class OrderManager:
    
    def __init__(self):
        self.__order_repo = OrderRepo()
        self.__temp_id = ""
        self.__temp_customer = ""
        self.__temp_start_date = ""
        self.__temp_end_date = ""
        self.__temp_pick_up_time = ""
        self.__temp_returning_time = ""
        self.__temp_pick_up_location = ""
        self.__temp_return_location = ""
        self.__temp_car_number = ""
        self.__temp_insurence = ""
        self.__temp_type_of_vehicle = ""
        self.__locations = ["reykjavik", "akureyri"]
    
    def get_order_list(self):
        return self.__order_repo.get_order_list()

    def get_dates(self):
        return self.__temp_start_date, self.__temp_end_date

    def get_type(self):
        return self.__temp_type_of_vehicle

    def save_new_order(self):
        # uses the temp values to save the new customer
        start_day = str(self.__temp_start_date.day) + '.' + str(self.__temp_start_date.month) + '.' + str(self.__temp_start_date.year)
        end_day = str(self.__temp_end_date.day) + '.' + str(self.__temp_end_date.month) + '.' + str(self.__temp_end_date.year)
        self.__order_repo.save_new_order(
            self.__temp_ID,
            self.__temp_ssn,
            start_day,
            end_day,
            self.__temp_pick_up_time,
            self.__temp_returning_time,
            self.__temp_pick_up_location,
            self.__temp_return_location,
            self.__temp_number_plate,
            self.__temp_insurance,
            self.__temp_type_of_vehicle)

    def get_inputted_order(self):
        print("Enter ID: {}".format(self.__temp_ID))
        print("Enter SSN: {}".format(self.__temp_ssn))
        print("Enter start date: {}".format(self.__temp_start_date))
        print("Enter ending date: {}".format(self.__temp_end_date))
        print("Enter pick up time: {}".format(self.__temp_pick_up_time))
        print("Enter returning time: {}".format(self.__temp_returning_time))
        print("Enter pick up location: {}".format(self.__temp_pick_up_location))
        print("Enter return location: {}".format(self.__temp_return_location))
        print("Enter type of vehicle: {}".format(self.__temp_type_of_vehicle))
        print("Enter number plate: {}".format(self.__temp_number_plate))
        print("Enter Insurance: {}".format(self.__temp_insurance))
        print()
        

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

    def get_number_plate(self):
        return self.__temp_number_plate

    def calculate_order(self):
        start_date_Input = self.__temp_start_date
        end_date_Input = self.__temp_end_date

        order_instance=Vehicle(0,0,0,0,self.__temp_type_of_vehicle,0,0,0)
        
        price_per_day=order_instance.get_price_per_day()

        price_per_day = order_instance.get_price_per_day()

        diffrence = end_date_Input - start_date_Input
        total = diffrence.days + 1
        return "Price is: {} ISK".format(price_per_day * total)

    def check_ID(self, ID, ignore_empty_value=False, current_value=''):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""
        if ID.strip() == '' and not ignore_empty_value:
            return self.error('ID')
        elif ID.strip() == '':
            self.__temp_ID = current_value
            return None
        ID = ID.replace("-", "")
        for letter in ID:
            if letter in (string.ascii_letters + string.punctuation):
                return "ID not valid. Please use only numbers."
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
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation):
                return "SSN not valid. Please use only numbers."
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
            return "Type not valid. Please enter one of the given types."

    def check_start_date(self, start_date, ignore_empty_value=False, current_value=''):
        """Check if start date is valid. Returns an error message if start date
        can not be converted to a datetime object"""
        if start_date.strip() == '' and not ignore_empty_value:
            return self.error('Start date')
        elif start_date.strip() == '':
            self.__temp_start_date = current_value
            return None
        present_day = date.today()
        try:
            year = start_date[6:]
            month = start_date[3:5]
            day = start_date[:2]
            date_object = date(int(year), int(month), int(day))
            if date_object < present_day:
                raise ValueError
            self.__temp_start_date = date_object
        except ValueError:
            return "Start date not valid. Please try again."

    def check_ending_date(self, end_date, ignore_empty_value=False, current_value=''):
        """Check if end date is valid. Returns an error message if end date
        can not be converted to a datetime object"""
        if end_date.strip() == '' and not ignore_empty_value:
            return self.error('End date')
        elif end_date.strip() == '':
            self.__temp_end_date = current_value
            return None
        try:
            year = end_date[6:]
            month = end_date[3:5]
            day = end_date[:2]
            date_object = date(int(year), int(month), int(day))
            if date_object < self.__temp_start_date:
                raise ValueError
            self.__temp_end_date = date_object
        except ValueError:
            return "End date not valid. Please try again."

    def check_pick_up_time(self, pick_up_time, ignore_empty_value=False, current_value=''):
        """Check if pick up time is valid. Returns an error message if pick up time
        has letters in it"""
        if pick_up_time.strip() == '' and not ignore_empty_value:
            return self.error('Pick up time')
        elif pick_up_time.strip() == '':
            self.__temp_pick_up_time = current_value
            return None
        pick_up_time = pick_up_time.replace("-", "").strip()
        time_correct_format = ""
        for letter in pick_up_time:
            if letter in (string.ascii_letters):
                return "Pick up time not valid. Please use only numbers."
            else:
                time_correct_format += letter
        '''if len(time_correct_format) < 8:
            return "Not a valid date."
        time_correct_format = time_correct_format[4:] + "-"+time_correct_format[2:4]+ "-" +time_correct_format[:2]
        datetime_object = datetime.datetime.strptime(time_correct_format, "%Y-%m-%d")
        if datetime_object < present_day:
            return "Check another date."
        else:'''
        self.__temp_pick_up_time = time_correct_format

    def check_returning_time(self, returning_time, ignore_empty_value=False, current_value=''):
        """Check if returning time is valid. Returns an error message if returning time
        has letters in it"""
        if returning_time.strip() == '' and not ignore_empty_value:
            return self.error('Return time')
        elif returning_time.strip() == '':
            self.__temp_returning_time = current_value
            return None
        returning_time = returning_time.replace("-", "")
        for letter in returning_time:
            if letter in (string.ascii_letters):
                return "Returning time not valid. Please use only numbers."
        self.__temp_returning_time = returning_time

    def check_pick_up_location(self, pick_up_location, ignore_empty_value=False, current_value=''):
        if pick_up_location.strip() == '' and not ignore_empty_value:
            return self.error('Pick up location')
        elif pick_up_location.strip() == '':
            self.__temp_pick_up_location = current_value
            return None
        if pick_up_location in self.__locations:
            self.__temp_pick_up_location = pick_up_location
        else:
            return "Please enter one of our locations."

    def check_return_location(self, return_location, ignore_empty_value=False, current_value=''):
        if return_location.strip() == '' and not ignore_empty_value:
            return self.error('Return location')
        elif return_location.strip() == '':
            self.__temp_return_location = current_value
            return None
        if return_location in self.__locations:
            self.__temp_return_location = return_location
        else:
            return "Please enter one of our locations."

    def check_number_plate(self, number_plate, ignore_empty_value=False, current_value=''):
        if number_plate.strip() == '' and not ignore_empty_value:
            return self.error('Number plate')
        elif number_plate.strip() == '':
            self.__temp_number_plate = current_value
            return None

        number_plate = number_plate.replace("-", "")
        for letter in number_plate:
            if letter in (string.punctuation):
                return "Number plate not valid. Please use only letters and numbers."
        self.__temp_number_plate = number_plate

    def check_insurance(self, insurance, ignore_empty_value=False, current_value=''):
        if insurance.strip() == '' and not ignore_empty_value:
            return self.error('Insurance')
        elif insurance.strip() == '':
            self.__temp_insurance = current_value
            return None
        insurance = insurance.strip()
        if insurance.lower() == "yes" or insurance.lower() == "no":
            self.__temp_insurance = insurance
        else:
            return "Please enter either Yes or No for insurance."

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
            if order.__str__().lower() == ID.lower():
                return order

    def delete_order(self, order):
        self.__order_repo.delete_order(order)
    
    def error(self, input_type):
        return '{} not valid. Please try again.'.format(input_type)
