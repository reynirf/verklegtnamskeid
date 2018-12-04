class Order:
    def __init__(self, order_id, employee, customer, vehicle, 
        start_time, end_time, pick_up, drop_off, insurance):
        self.__order_id = order_id
        self.__employee = employee
        self.__customer = customer
        self.__vehicle = vehicle
        self.__start_time = start_time
        self.__end_time = end_time
        self.__pick_up = pick_up
        self.__drop_off = drop_off
        self.__insurance = insurance
    
    def __str__(self):
        return self.__order_id