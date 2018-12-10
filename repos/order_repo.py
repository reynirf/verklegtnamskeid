from models.employee import Employee
from models.order import Order
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
                        line['ssn'], 
                        line['starting date'], 
                        line['ending date'],
                        line['pick up time'],
                        line['returning time'],
                        line['pick up location'],
                        line['return location'],
                        line['number plate'],
                        line['insurance'],
                        line['type of vehicle'])
                    self.__order_list.append(order)
        return self.__order_list

    def set_current_order(self, order):
        self.__current_order = order

    def get_current_order(self):
        return self.__current_order

    def save_new_order(self, ID, ssn, starting_date, ending_date, pick_up_time,
                       returning_time, pick_up_location, return_location, car_number, insurance,
                       type_of_vehicle):
        with open(self.ORDER_FILE, 'a', newline='') as order_file:
            csv_writer = csv.writer(order_file)
            csv_writer.writerow([ID, ssn, starting_date, ending_date, pick_up_time,
                                 returning_time, pick_up_location, return_location, car_number,
                                 insurance, type_of_vehicle])
        self.__order_list = []

    def delete_order(self, order):
        """Deletes order from file"""
        file_content = []
        with open(self.ORDER_FILE, 'r') as order_file:
            csv_reader = csv.reader(order_file)
            for line in csv_reader:
                if line != []:
                    if line[0] != order.__str__():
                        file_content.append(line)
        with open(self.ORDER_FILE, 'w', newline='') as updated_file:
            csv_writer = csv.writer(updated_file)
            for line in file_content:
                csv_writer.writerow(line)
        self.__order_list = []