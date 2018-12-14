from repos.customer_repo import CustomerRepo
from models.customer import Customer
from datetime import date
import string


class CustomerManager:

    def __init__(self):
        self.__customer_repo = CustomerRepo()
        self.__temp_name = ""
        self.__temp_ssn = ""
        self.__temp_phone = ""
        self.__temp_driver_license = ""
        self.__temp_email = ""
        self.__temp_credit_card = ""
        self.__temp_address = ""

    def get_customer_list(self):
        return self.__customer_repo.get_customer_list()

    def save_new_customer(self):
        """uses the temp values to save the new customer """
        self.__customer_repo.save_new_customer(
            self.__temp_name,
            self.__temp_ssn,
            self.__temp_phone,
            self.__temp_email,
            self.__temp_address,
            self.__temp_driver_license,
            self.__temp_credit_card
        )

    def check_name(self, name, ignore_empty_value=False, current_value=""):
        """check if name is valid. Returns an error message if name
        has numbers or punctuation in it. When editing a customer a 
        previous value is used if nothing is entered.
        """
        if name.strip() == "" and not ignore_empty_value:
            return self.error("Name")
        elif name.strip() == "":
            self.__temp_name = current_value
            return None
        
        for letter in name.strip():
            if letter in (string.digits + string.punctuation):
                return self.error("Name")
        self.__temp_name = name

    def check_ssn(self, ssn, ignore_empty_value=False, current_value=""):
        """Check if ssn is valid. Returns an error message if ssn
        has letters or punctuation in it. When editing a customer a 
        previous value is used if nothing is entered.
        """
        ssn = ssn.replace("-", "").replace(" ", "")
        
        if self.find_customer_by_ssn(ssn) and not current_value:
            return "Customer with this SSN has already been registered"
        if ssn.strip() == "" and not ignore_empty_value:
            return self.error("SSN")
        elif ssn.strip() == "":
            self.__temp_ssn = current_value
            return None
        
        elif len(ssn.strip()) < 7:
            return self.error("SSN")
        for letter in ssn:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error("SSN")
        self.__temp_ssn = ssn

    def check_phone_number(self, phone, ignore_empty_value=False, current_value=""):
        """Check if phone number is valid. Returns an error message if phone
        number has letters or punctuation in it. When editing a customer a 
        previous value is used if nothing is entered.
        """
        phone = phone.replace("-", "")
        
        if phone.strip() == "" and not ignore_empty_value:
            return self.error("Phone number")
        elif phone.strip() == "":
            self.__temp_phone = current_value
            return None
        
        for letter in phone:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error("Phone number")
        self.__temp_phone = phone

    def check_license(self, driver_license, ignore_empty_value=False, current_value=""):
        """Check if driver license categories given are valid. Returns an 
        error message if categories given are not valid. When editing a customer 
        a previous value is used if nothing is entered.
        """
        categories = ["a", "a1", "b", "be", "c1", "c1e", "c", "ce", "d1", "d1e", "d", "de"]
        driver_license = driver_license.split()

        if not driver_license and not ignore_empty_value:
            return self.error("Driver license category")
        elif not driver_license:
            self.__temp_driver_license = current_value
            return None
        for char in driver_license:
            if char.lower() not in categories:
                return self.error("Driver license category")
        self.__temp_driver_license = driver_license[0]

    def check_email(self, email, ignore_empty_value=False, current_value=""):
        """Check if email address is valid. Returns an error message if email 
        does not have an @ and "." in it or if it is too short. When editing 
        a previous value is used if nothing is entered.
        """
        condition = "@" not in email or len(email) < 6 or "." not in email
        
        if condition and not ignore_empty_value:
            return self.error("Email")
        elif email == "" and ignore_empty_value:
            self.__temp_email = current_value
            return None
        elif condition:
            return self.error("Email")
        self.__temp_email = email

    def check_credit_card(self, credit_card, ignore_empty_value=False, current_value=""):
        """Check if credit card number is valid. Returns an error message if 
        credit card number has letters or punctuation in it or if it is too 
        short. When editing a previous value is used if nothing is entered.
        """
        credit_card = credit_card.replace("-", "").replace(" ", "")

        if len(credit_card) != 16 and not ignore_empty_value:
            return self.error("Credit card number")
        elif len(credit_card) == 0:
            self.__temp_credit_card = current_value
            return None
        elif len(credit_card) != 16:
            return self.error("Credit card number")
        
        for letter in credit_card:
            if letter in (string.ascii_letters + string.punctuation):
                return self.error("Credit card number")
        self.__temp_credit_card = credit_card

    def check_address(self, address, ignore_empty_value=False, current_value=""):
        """Checks that address is at least 5 letters long. When editing a
        previous value is used if nothing is entered.
        """
        if address.strip() == "" and not ignore_empty_value:
            return self.error("Home address")
        elif address.strip() == "":
            self.__temp_address = current_value
            return None
        
        if len(address) < 5:
            return self.error("Home address")
        self.__temp_address = address

    def find_customer_by_name(self, name):
        """Searches through a list of customers to find those whose name 
        matches the given name. Returns a list of matched customers or
        None if no customers are found.
        """
        customer_list = self.__customer_repo.get_customer_list()
        customers = []
        for customer in customer_list:
            if name.lower() in customer.__str__().lower():
                customers.append(customer)
        if customers != []:
            return customers

    def find_customer_by_ssn(self, ssn):
        """Searches through a list of customers to find those whose SSN 
        matches the given SSN. Returns a list of matched customers or
        None if no customers are found.
        """
        customer_list = self.__customer_repo.get_customer_list()
        ssn = ssn.replace("-", "")
        for customer in customer_list:
            customer_ssn = customer.get_ssn()
            if customer_ssn == ssn:
                return customer

    def delete_customer(self, customer):
        self.__customer_repo.delete_customer(customer)

    def error(self, input_type):
        """An error message used by all check methods"""
        return "{} not valid. Please try again.".format(input_type)
