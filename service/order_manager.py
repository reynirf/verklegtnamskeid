from repos.order_repo import OrderRepo
from models.order import Order
import string
<<<<<<< HEAD
from models.vehicle import Vehicle
=======
import datetime
>>>>>>> a477c13f62b4e972f35a33659ecae1814a57b04d

class OrderManager:

    def __init__(self):
        self.__order_repo = OrderRepo()
        self.__temp_id = ""
        self.__temp_customer = ""
        self.__temp_starting_date = ""
        self.__temp_ending_date = ""
        self.__temp_pick_up_time = ""
        self.__temp_returning_time = ""
        self.__temp_pick_up_location = ""
        self.__temp_return_location = ""
        self.__temp_number_of_seats = ""
        self.__temp_car_number = ""
        self.__temp_insurence = ""
    
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
            self.__temp_insurance)

    def calculate_order(self):
        price_per_day = Vehicle.get_price_per_day(self.__temp_number_plate)
        start = self.__temp_start_date
        end = self.__temp_ending_date


    def check_ID(self,ID):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""
        ID = ID.replace("-", "")
        for letter in ID:
            if letter in (string.ascii_letters + string.punctuation):
                return "ID not valid. Please use only numbers."
        self.__temp_ID = ID

    def check_ssn(self,ssn):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""
        ssn = ssn.replace("-", "")
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation):
                return "SSN not valid. Please use only numbers."
        self.__temp_ssn = ssn
    
    def check_make(self,make):
        """check if make is valid. Returns an error message if make
        has numbers or punctuation in it"""
        for letter in make.strip():
            if letter in (string.digits + string.punctuation):
                return "Make not valid. Please use only letters."
        self.__temp_car = make

    def check_start_date(self,start_date):
        """Check if start date is valid. Returns an error message if start date
        has letters in it"""
        present_day = datetime.date.today()
        start_date = start_date.replace("-", "")
        for letter in start_date:
            if letter in (string.ascii_letters):
                return "Start date not valid. Please use only numbers."
        self.__temp_start_date = start_date

    def check_ending_date(self,end_date):
        """Check if ending date is valid. Returns an error message if ending date
        has letters in it"""
        end_date = end_date.replace("-", "")
        for letter in end_date:
            if letter in (string.ascii_letters):
                return "Ending date not valid. Please use only numbers."
        self.__temp_end_date = end_date

    def check_pick_up_time(self,pick_up_time):

        present_day = datetime.datetime.today()
        """Check if pick up time is valid. Returns an error message if pick up time
        has letters in it"""
        pick_up_time = pick_up_time.replace("-", "").strip()
        time_correct_format = ""
        for letter in pick_up_time:
            if letter in (string.ascii_letters):
                return "Pick up time not valid. Please use only numbers."
            else:
                time_correct_format += letter
        if len(time_correct_format) < 8:
            return "Not a valid date."
        time_correct_format = time_correct_format[4:] + "-"+time_correct_format[2:4]+ "-" +time_correct_format[:2]
        datetime_object = datetime.datetime.strptime(time_correct_format, "%Y-%m-%d")
        if datetime_object < present_day:
            return "Check another date."
        else:
            self.__temp_pick_up_time = time_correct_format

    def check_returning_time(self,returning_time):
        """Check if returning time is valid. Returns an error message if returning time
        has letters in it"""
        returning_time = returning_time.replace("-", "")
        for letter in returning_time:
            if letter in (string.ascii_letters):
                return "Returning time not valid. Please use only numbers."
        self.__temp_returning_time = returning_time

    def check_pick_up_location(self,pick_up_location):
        self.__temp_pick_up_location = pick_up_location
    
    def check_return_location(self,return_location):
        self.__temp_return_location = return_location
    
    def check_number_of_seats(self,number_of_seats):
        """Check if number of seats is valid. Returns an error message if number of seats
        has letters or punctuation in it"""
        number_of_seats = number_of_seats.replace("-", "")
        for letter in number_of_seats:
            if letter in (string.ascii_letters + string.punctuation):
                return "Number of seats not valid. Please use only numbers."
        self.__temp_number_of_seats = number_of_seats

    def check_number_plate(self,number_plate):
        self.__temp_number_plate = number_plate
    
    def check_insurance(self,insurance):
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