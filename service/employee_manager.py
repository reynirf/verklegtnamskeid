from repos.employee_repo import EmployeeRepo

class EmployeeManager:

    def __init__(self):
        self.__employee_repo = EmployeeRepo()