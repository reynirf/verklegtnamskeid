from repos.employee_repo import EmployeeRepo
from models.employee import Employee


class EmployeeManager:

    def __init__(self):
        self.__employee_repo = EmployeeRepo()
        self.__has_failed_auth = False

    def authenticate(self, employee_id, employee_password):
        empoloyee_list = self.__employee_repo.get_employee_list()
        for employee in empoloyee_list:
            if employee.get_id() == employee_id:
                if employee.get_password() == employee_password:
                    self.__employee_repo.set_current_employee(employee)
                    return employee
                else:
                    self.__has_failed_auth = True
                    return "Wrong password"
        self.__has_failed_auth = True
        return "Invalid ID: " + employee_id

    def get_employee_list(self):
        return self.__employee_repo.get_employee_list()

    def has_failed(self):
        return self.__has_failed_auth

    def get_current_employee(self):
        return self.__employee_repo.get_current_employee()
