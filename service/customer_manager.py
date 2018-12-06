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
    
    def check_name(self, name):
        """check if name is valid. Returns an error message if name
        has numbers or punctuation in it"""

        for letter in name.strip():
            if letter in (string.digits + string.punctuation):
                return "Name not valid. Please use only letters."
        self.__temp_name = name
    
    def check_ssn(self, ssn):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it"""

        ssn = ssn.replace("-", "")
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation) or ssn.strip() == '':
                return "SSN not valid. Please try again."
        self.__temp_ssn = ssn

    def check_birthday(self, birthday):
        #missing check for invalid birthday
        if birthday.strip() == '':
            return 'Birthday not valid. Please try Again'
        self.__temp_birthday = birthday
        return None
    
    def check_phone_number(self, phone):
        """Check if phone number is valid. Returns an error message if phone
        number has letters or punctuation in it"""

        phone = phone.replace("-", "")
        for letter in phone:
            if letter in (string.ascii_letters + string.punctuation) or phone.strip() == '':
                return "Phone number not valid. Please use only numbers."
        self.__temp_phone = phone

    def check_license(self, driver_license):
        """Check if driver license categories given are valid. Returns an 
        error message if categories given are not valid."""

        valid_categories = ["a", "a1", "b", "be", "c1", "c1e", "c", "ce", "d1", "d1e", "d", "de"]
        driver_license = driver_license.split()
        for char in driver_license:
            if char.lower() not in valid_categories:
                return "Driver license category not valid. Please try again."
        self.__temp_driver_license = driver_license
    
    def check_email(self, email):
        """Check if email address is valid. Returns an error message if email
        does not have an '@' in it"""

        if "@" not in email or len(email) < 6 or '.' not in email:
            return "Email not valid. Please try again"
        self.__temp_email = email
    
    def check_credit_card(self, credit_card):
        """Check if credit card number is valid. Returns an error message if 
        credit card number has letters or punctuation in it"""

        credit_card = credit_card.replace("-", "").replace(' ', '') 
        for letter in credit_card:
            if letter in (string.ascii_letters + string.punctuation) or len(credit_card) != 16:
                return "Credit card number not valid. Please try again."
        self.__temp_credit_card = credit_card
    
    def check_address(self, address):
        #missing check for invalid address
        if address.strip() == '':
            return 'Home address not valid. Please try again.'
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