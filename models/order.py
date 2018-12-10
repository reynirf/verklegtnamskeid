from datetime import date

class Order:
    def __init__(self, order_id, ssn, start_date, end_date, 
            pick_up_time, return_time, pick_up_location, return_location, number_plate, insurance, vehicle_type):
        self.__order_id = order_id
        self.__ssn = ssn
        self.__start_date = date(int(start_date[6:]), int(start_date[3:5]), int(start_date[:2]))
        self.__end_date = date(int(end_date[6:]), int(end_date[3:5]), int(end_date[:2]))
        self.__pick_up_time = pick_up_time
        self.__return_time = return_time
        self.__pick_up_location = pick_up_location
        self.__return_location = return_location
        self.__number_plate = number_plate 
        self.__insurance = insurance
        self.__vehicle_type = vehicle_type
    
    def __str__(self):
        return self.__order_id
    
    def get_ssn(self):
        return self.__ssn
    
    def get_dates(self):
        return self.__start_date, self.__end_date
    
    def get_number_plate(self):
        return self.__number_plate
    
    def return_details(self):
        """Returns the details needed for editing the order"""
        start_day = str(self.__start_date.day) + '.' + str(self.__start_date.month) + '.' + str(self.__start_date.year)
        end_day = str(self.__end_date.day) + '.' + str(self.__end_date.month) + '.' + str(self.__end_date.year)
        return {
            "ID": self.__order_id,
            "SSN": self.__ssn,
            "Start date": start_day,
            "End date": end_day,
            "Pick up time": self.__pick_up_time,
            "Return time": self.__return_time,
            "Pick up location": self.__pick_up_location,
            "Return location": self.__return_location,
            "Type": self.__vehicle_type,
            "Number plate": self.__number_plate,
            "Insurance": self.__insurance
        }

