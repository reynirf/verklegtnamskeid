from models.employee import Employee
import csv

class OrderRepo:

    ORDER_FILE = "./data/orders.csv"

    def __init__(self):
        self.__order_list = []
        self.__current_order = ""
    
    def get_order_list(self):
        """Returns a list of all orders on file"""
        if self.__order_list == []:
            with open(self.ORDER_FILE, 'r') as order_file:
                csv_reader = csv.DictReader(order_file)
                for line in csv_reader:
                    order = Order(
                        line['id'],
                        line['customer'], 
                        line['starting date'], 
                        line['ending date'].
                        line['pick up time'],
                        line['returning time'],
                        line['pick up location'],
                        line['return location'],
                        line['number of seats'],
                        line['car number'],
                        line['insurance'])
                    self.__order_list.append(order)
        return self.__order_list
    
    def set_current_order(self, order):
        self.__current_order = order

    def get_current_order(self):
        return self.__current_order