from repos.employee_repo import EmployeeRepo
from models.employee import Employee

class EmployeeManager:

    def __init__(self):
        self.__employee_repo = EmployeeRepo()
    
    def authenticate(self, employee_id, employee_password):
        empoloyee_list = self.__employee_repo.get_employee_list()
        for employee in empoloyee_list:
            if employee.get_id() == employee_id:
                if employee.get_password() == employee_password:
                    return employee
                else:
                    return "Wrong password"
        return "Invalid id"
    
    def get_employee_list(self):
        return self.__employee_repo.get_employee_list()