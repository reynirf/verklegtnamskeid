from models.customer import Customer
import csv

class CustomerRepo:

    CUSTOMER_FILE = "./data/customers.csv"

    def __init__(self):
        self.__customer_list = []

    def get_customer_list(self):
        """Returns a list of all customers on file"""
        if self.__customer_list == []:
            with open(self.CUSTOMER_FILE, 'r') as customer_file:
                csv_reader = csv.DictReader(customer_file)
                for line in csv_reader:
                    customer = Customer(
                        line['name'],
                        line['ssn'], 
                        line['birthday'], 
                        line['phone'],
                        line['email'],
                        line['address'], 
                        line['driver licence'], 
                        line['credit card'])
                    self.__customer_list.append(customer)
        return self.__customer_list