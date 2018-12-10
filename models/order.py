class Order:
    def __init__(self, order_id, ssn,
        start_date, end_date, pick_up_time, return_time, pick_up_location, return_location, number_plate, insurance, vehicle_type):
        self.__order_id = order_id
        self.__ssn = ssn
        self.__start_date = start_date
        self.__end_date = end_date
        self.__pick_up_time = pick_up_time
        self.__return_time = return_time
        self.__pick_up_location = pick_up_location
        self.__return_location = return_location
        self.__number_plate = number_plate 
        self.__insurance = insurance
    
    def __str__(self):
        return self.__order_id
    
    def get_ssn(self):
        return self.__ssn
    
    def get_dates(self):
        return self.__start_date, self.__end_date
    
    def get_number_plate(self):
        return self.__number_plate
