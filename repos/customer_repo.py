from models.customer import Customer
import csv


class CustomerRepo:
    CUSTOMER_FILE = "./data/customers.csv"

    def __init__(self):
        self.__customer_list = []

    def get_customer_list(self):
        """Reads in all customers on file and returns a list of 
        Customer instances"""
        if self.__customer_list == []:
            with open(self.CUSTOMER_FILE, "r") as customer_file:
                csv_reader = csv.DictReader(customer_file)
                for line in csv_reader:
                    customer = Customer(
                        line["name"],
                        line["ssn"],
                        line["phone"],
                        line["email"],
                        line["address"],
                        line["driver license"],
                        line["credit card"])
                    self.__customer_list.append(customer)
        return self.__customer_list

    def save_new_customer(self, name, ssn, phone, email, address, driver_licence, credit_card):
        """Writes details of a new customer to file"""
        with open(self.CUSTOMER_FILE, "a", newline="") as customer_file:
            csv_writer = csv.writer(customer_file)
            csv_writer.writerow([
                name, 
                ssn, 
                phone, 
                email, 
                address, 
                driver_licence, 
                credit_card
            ])
        self.__customer_list = []

    def delete_customer(self, customer):
        """Reads customers from file and compares with customer. Writes the
        file again without the line that matches the SSN.
        """
        file_content = []
        with open(self.CUSTOMER_FILE, "r") as customer_file:
            csv_reader = csv.reader(customer_file)
            for line in csv_reader:
                # compares second column of non empty lines to customer SSN
                if line != []:
                    if line[1] != customer.get_ssn():
                        file_content.append(line)
        with open(self.CUSTOMER_FILE, "w", newline="") as updated_file:
            csv_writer = csv.writer(updated_file)
            for line in file_content:
                csv_writer.writerow(line)
        self.__customer_list = []
