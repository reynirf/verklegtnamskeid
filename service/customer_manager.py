from repos.customer_repo import CustomerRepo
from models.customer import Customer

class CustomerManager:

    def __init__(self):
        self.__customer_repo = CustomerRepo()
        self.__temp_name = ""
        self.__temp_ssn = ""
        self.__birthday = ""
        self.__phone = ""
        self.__driver_license = ""
        self.__email = ""
        self.__credit_card = ""
        self.__address = ""
    
    def get_customer_list(self):
        return self.__customer_repo.get_customer_list()
    
    def save_new_customer(self):
        #uses the temp values to save the new customer and then clears them
        pass
    
    def check_name(self, name):
        #missing check for invalid names
        self.__temp_name = name
    
    def check_ssn(self, ssn):
        #missing check for invalid ssn
        self.__temp_ssn = ssn

    def check_birthday(self, birthday):
        #missing check for invalid birthday
        self.__birthday = birthday
    
    def check_phone_number(self, phone):
        #missing check for invalid phone number
        self.__phone = phone

    def check_license(self, driver_license):
        #missing check for invalid driver license category
        self.__driver_license = driver_license
    
    def check_email(self, email):
        #missing check for invalid email
        self.__email = email
    
    def check_credit_card(self, credit_card):
        #missing check for invalid credit card
        self.__credit_card = credit_card
    
    def check_address(self, address):
        #missing check for invalid address
        self.__address = address