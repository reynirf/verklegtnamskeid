from repos.customer_repo import CustomerRepo
from models.customer import Customer
import string

class CustomerManager:

    def __init__(self):
        self.__customer_repo = CustomerRepo()
        self.__temp_name = ""
        self.__temp_ssn = ""
        self.__temp_birthday = ""
        self.__temp_phone = ""
        self.__temp_driver_license = ""
        self.__temp_email = ""
        self.__temp_credit_card = ""
        self.__temp_address = ""
    
    def get_customer_list(self):
        return self.__customer_repo.get_customer_list()
    
    def save_new_customer(self):
        #uses the temp values to save the new customer 
        self.__customer_repo.save_new_customer(
            self.__temp_name,
            self.__temp_ssn,
            self.__temp_birthday,
            self.__temp_phone,
            self.__temp_email,
            self.__temp_address,
            self.__temp_driver_license,
            self.__temp_credit_card)
    
    def return_details(self):
        return {
            "Name": self.__temp_name,
            "SSN": self.__temp_ssn,
            "Birthday": self.__temp_birthday,
            "Phone number": self.__temp_phone,
            "Email address": self.__temp_email,
            "Home address": self.__temp_address,
            "Driver license category": self.__temp_driver_license,
            "Credit card number": self.__temp_credit_card
        }
    
    def check_name(self, name):
        """check if name is valid. Returns an error message if name
        has numbers or punctuation in it"""

        if name.strip() == '':
                return self.error('Name')
        for letter in name.strip():
            if letter in (string.digits + string.punctuation):
                return self.error('Name')
        self.__temp_name = name
    
    def check_ssn(self, ssn):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""

        ssn = ssn.replace("-", "")
        if ssn.strip() == '':
            return self.error('SSN')
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error('SSN')
        self.__temp_ssn = ssn

    def check_birthday(self, birthday):
        #missing check for invalid birthday
        if birthday.strip() == '':
            return self.error('Birthday')
        self.__temp_birthday = birthday
        return None
    
    def check_phone_number(self, phone):
        """Check if phone number is valid. Returns an error message if phone
        number has letters or punctuation in it"""

        phone = phone.replace("-", "")
        if phone.strip() == '':
            return self.error('Phone number')
        for letter in phone:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error('Phone number')
        self.__temp_phone = phone

    def check_license(self, driver_license):
        """Check if driver license categories given are valid. Returns an 
        error message if categories given are not valid."""

        valid_categories = ["a", "a1", "b", "be", "c1", "c1e", "c", "ce", "d1", "d1e", "d", "de"]
        driver_license = driver_license.split()
        if driver_license.strip() == '':
            return self.error('Driver license category')
        for char in driver_license:
            if char.lower() not in valid_categories:
                return self.error('Driver license category')
        self.__temp_driver_license = driver_license[0]
    
    def check_email(self, email):
        """Check if email address is valid. Returns an error message if email 
        does not have an @ in it"""

        if "@" not in email or len(email) < 6 or '.' not in email:
            return self.error('Email')
        self.__temp_email = email
    
    def check_credit_card(self, credit_card):
        """Check if credit card number is valid. Returns an error message if 
        credit card number has letters or punctuation in it"""

        credit_card = credit_card.replace("-", "").replace(' ', '') 
        if len(credit_card) != 16:
            return self.error('Credit card number')
        for letter in credit_card:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error('Credit card number')
        self.__temp_credit_card = credit_card
    
    def check_address(self, address):
        #missing check for invalid address
        if address.strip() == '':
            return self.error('Home address')
        self.__temp_address = address


    def find_customer_by_name(self, name):
        customer_list = self.__customer_repo.get_customer_list()
        customers = []
        for customer in customer_list:
            if customer.__str__().lower() == name.lower():
                customers.append(customer)
        if customers != []:
            return customers

    def find_customer_by_ssn(self, ssn):
        customer_list = self.__customer_repo.get_customer_list()
        ssn = ssn.replace("-", "")
        for customer in customer_list:
            customer_ssn = customer.get_ssn().replace("-", "")
            if customer_ssn == ssn:
                return customer

    def error(self, input_type):
        return '{} not valid. Please try again.'.format(input_type)