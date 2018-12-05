from repos.order_repo import OrderRepo
from models.order import Order

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
        self.__order_repo.save_new_car(
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
            self.__temp_insurence)

    def check_id(self,ID):
        self.__temp_ID = ID

    def check_ssn(self,ssn):
        self.__temp_ssn = ssn
    
    def check_car(self,car):
        self.__temp_car = car

    def check_start_date(self,start_date):
        self.__temp_start_date = start_date

    def check_ending_date(self,end_date):
        self.__temp_end_date = end_date

    def check_pick_up_time(self,pick_up_time):
        self.__temp_pick_up_time = pick_up_time

    def check_returning_time(self,returning_time):
        self.__temp_returning_time = returning_time

    def check_pick_up_location(self,pick_up_location):
        self.__temp_pick_up_location = pick_up_location
    
    def check_return_location(self,return_location):
        self.__temp_return_location = return_location
    
    def check_number_of_seats(self,number_of_seats):
        self.__temp_number_of_seats = number_of_seats

    def check_number_plate(self,number_plate):
        self.__temp_number_plate = number_plate
    
    def check_insurance(self,insurence):
        self.__temp_insurence = insurence