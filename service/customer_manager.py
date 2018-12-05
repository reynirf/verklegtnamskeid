from repos.customer_repo import CustomerRepo
from models.customer import Customer

class CustomerManager:

    def __init__(self):
        self.__customer_repo = CustomerRepo()
        self.__temp_name = ""
        self.__temp_ssn = ""
    
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