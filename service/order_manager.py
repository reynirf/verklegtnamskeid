from repos.order_repo import OrderRepo
from models.order import Order
import string
from models.vehicle import Vehicle
import datetime
from datetime import date
import time

class OrderManager:

    def __init__(self):
        self.__order_repo = OrderRepo()
        self.__temp_id = ""
        self.__temp_customer = ""
        self.__temp_start_date = ""
        self.__temp_ending_date = ""
        self.__temp_pick_up_time = ""
        self.__temp_returning_time = ""
        self.__temp_pick_up_location = ""
        self.__temp_return_location = ""
        self.__temp_number_of_seats = ""
        self.__temp_car_number = ""
        self.__temp_insurence = ""
        self.__temp_type_of_vehicle = ""
    
    def get_order_list(self):
        return self.__order_repo.get_order_list()

    def save_new_order(self):
        #uses the temp values to save the new customer and then clears them 
        self.__order_repo.save_new_order(
            self.__temp_ID,
            self.__temp_ssn,
            self.__temp_car,
            self.__temp_start_date,
            self.__temp_end_date,
            self.__temp_pick_up_time,
            self.__temp_returning_time,
            self.__temp_pick_up_location,
            self.__temp_return_location,
            self.__temp_number_of_seats,
            self.__temp_number_plate,
            self.__temp_insurance,
            self.__temp_type_of_vehicle)

    def get_inputted_order(self):
        print("{}".format(self.__temp_ID))
        print("{}".format(self.__temp_ssn))
        print("{}".format(self.__temp_car))
        #print("{}".format(self.__temp_start_date))
        #print("{}".format(self.__temp_end_date))
        print("{}".format(self.__temp_pick_up_time))
        print("{}".format(self.__temp_returning_time))
        print("{}".format(self.__temp_pick_up_location))
        print("{}".format(self.__temp_return_location))
        print("{}".format(self.__temp_number_of_seats))
        print("{}".format(self.__temp_number_plate))
        print("{}".format(self.__temp_insurance))
        print("{}".format(self.__temp_type_of_vehicle))

    def get_order_dates(self):
        dates = []
        working_date = self.__temp_start_date
        while working_date <= self.__temp_end_date:
            dates.append(working_date)
            x = working_date.day + 1
            working_date.replace(day=x)
        return dates, self.__temp_number_plate

    def calculate_order(self):
        start_date_Input = self.__temp_start_date
        end_date_Input = self.__temp_end_date

        order_instance=Vehicle(0,self.__temp_car,0,self.__temp_type_of_vehicle,0,self.__temp_number_of_seats,0,0)
        
        price_per_day=order_instance.get_price_per_day()

        diffrence = end_date_Input - start_date_Input 
        total=diffrence.days + 1
        return "Price is: {}".format(price_per_day*total)


    def check_ID(self,ID, ignore_empty_value = False, current_value = ''):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""
        ID = ID.replace("-", "")
        for letter in ID:
            if letter in (string.ascii_letters + string.punctuation):
                return "ID not valid. Please use only numbers."
        self.__temp_ID = ID

    def check_ssn(self,ssn, ignore_empty_value = False, current_value = ''):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""
        ssn = ssn.replace("-", "")
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation):
                return "SSN not valid. Please use only numbers."
        self.__temp_ssn = ssn
    
    def check_make(self,make, ignore_empty_value = False, current_value = ''):
        """check if make is valid. Returns an error message if make
        has numbers or punctuation in it"""
        for letter in make.strip():
            if letter in (string.digits + string.punctuation):
                return "Make not valid. Please use only letters."
        self.__temp_car = make

    def check_type_of_vehicle(self,type_of_vehicle, ignore_empty_value = False, current_value = ''):
        """check if make is valid. Returns an error message if make
        has numbers or punctuation in it"""
        for letter in type_of_vehicle.strip():
            if letter in (string.digits + string.punctuation):
                return "Make not valid. Please use only letters."
        self.__temp_type_of_vehicle = type_of_vehicle

    def check_start_date(self,start_date, ignore_empty_value = False, current_value = ''):
        """Check if start date is valid. Returns an error message if start date
        can not be converted to a datetime object"""
        present_day = datetime.date.today()
        try:
            year = start_date[6:]
            month = start_date[3:5]
            day = start_date[:2]
            date_object = datetime.date(int(year), int(month), int(day))
            if date_object < present_day:
                raise ValueError
            self.__temp_start_date = date_object
        except ValueError:
            return "Start date not valid. Please try again."
        
    def check_ending_date(self,end_date, ignore_empty_value = False, current_value = ''):
        """Check if end date is valid. Returns an error message if end date
        can not be converted to a datetime object"""
        try:
            year = end_date[6:]
            month = end_date[3:5]
            day = end_date[:2]
            date_object = datetime.date(int(year), int(month), int(day))
            if date_object < self.__temp_start_date:
                raise ValueError
            self.__temp_end_date = date_object
        except ValueError:
            return "End date not valid. Please try again."

    def check_pick_up_time(self,pick_up_time, ignore_empty_value = False, current_value = ''):
        """Check if pick up time is valid. Returns an error message if pick up time
        has letters in it"""
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

    def check_returning_time(self,returning_time, ignore_empty_value = False, current_value = ''):
        """Check if returning time is valid. Returns an error message if returning time
        has letters in it"""
        returning_time = returning_time.replace("-", "")
        for letter in returning_time:
            if letter in (string.ascii_letters):
                return "Returning time not valid. Please use only numbers."
        self.__temp_returning_time = returning_time

    def check_pick_up_location(self,pick_up_location, ignore_empty_value = False, current_value = ''):
        self.__temp_pick_up_location = pick_up_location
    
    def check_return_location(self,return_location, ignore_empty_value = False, current_value = ''):
        self.__temp_return_location = return_location
    
    def check_number_of_seats(self,number_of_seats, ignore_empty_value = False, current_value = ''):
        """Check if number of seats is valid. Returns an error message if number of seats
        has letters or punctuation in it"""
        number_of_seats = number_of_seats.replace("-", "")
        for letter in number_of_seats:
            if letter in (string.ascii_letters + string.punctuation):
                return "Number of seats not valid. Please use only numbers."
        self.__temp_number_of_seats = number_of_seats

    def check_number_plate(self,number_plate, ignore_empty_value = False, current_value = ''):
        self.__temp_number_plate = number_plate
    
    def check_insurance(self,insurance, ignore_empty_value = False, current_value = ''):
        self.__temp_insurance = insurance


    def find_order_by_ssn(self, ssn):
        order_list = self.__order_repo.get_order_list()
        ssn = ssn.replace("-", "")
        for order in order_list:
            order_ssn = order.get_ssn().replace("-", "")
            if order_ssn == ssn:
                return order
    def find_order_by_id(self, ID):
        order_list = self.__order_repo.get_order_list()
        orders = []
        for order in order_list:
            if order.__str__().lower() == ID.lower():
                orders.append(order)
        if orders != []:
            return orders