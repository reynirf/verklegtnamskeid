from repos.customer_repo import CustomerRepo
from models.customer import Customer

class CustomerManager:

    def __init__(self):
        self.__customer_repo = CustomerRepo()
    
    def get_customer_list(self):
        return self.__customer_repo.get_customer_list()