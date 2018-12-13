from datetime import date


class Order:
    def __init__(
        self, order_id, ssn, start_date, end_date, pick_up_time, return_time, 
        pick_up_location, return_location, license_plate, insurance, vehicle_type
    ):
        self.__order_id = order_id
        self.__ssn = ssn
        self.__start_date_str = start_date[6:] + "." + start_date[4:6] + "." + start_date[:4]
        self.__end_date_str = end_date[6:] + "." + end_date[4:6] + "." + end_date[:4]
        self.__start_date = date(
            int(start_date[:4]), int(start_date[4:6]), int(start_date[6:]))
        self.__end_date = date(
            int(end_date[:4]), int(end_date[4:6]), int(end_date[6:]))
        self.__pick_up_time = pick_up_time
        self.__return_time = return_time
        self.__pick_up_location = pick_up_location
        self.__return_location = return_location
        self.__license_plate = license_plate 
        self.__insurance = insurance
        self.__vehicle_type = vehicle_type
    
    def __str__(self):
        return "{} | {}".format(self.__order_id, self.__ssn)
    
    def get_ssn(self):
        return self.__ssn

    def get_id(self):
        return self.__order_id
    
    def get_dates(self):
        return self.__start_date, self.__end_date
    
    def get_date_str(self):
        return self.__start_date_str + " - " + self.__end_date_str
    
    def get_license_plate(self):
        return self.__license_plate
    
    def return_details(self):
        """ Returns the order details in a dictionary """
        return {
            "ID": self.__order_id,
            "SSN": self.__ssn,
            "Start date": self.__start_date_str,
            "End date": self.__end_date_str,
            "Pick up time": self.__pick_up_time,
            "Return time": self.__return_time,
            "Pick up location": self.__pick_up_location,
            "Return location": self.__return_location,
            "Type": self.__vehicle_type,
            "License plate": self.__license_plate,
            "Insurance": self.__insurance
        }

