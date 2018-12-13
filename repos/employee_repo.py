from models.employee import Employee
import csv


class EmployeeRepo:
    EMPLOYEE_FILE = "./data/employees.csv"

    def __init__(self):
        self.__employee_list = []
        self.__current_employee = ""

    def get_employee_list(self):
        """Reads in all employees on file and returns a list of 
        Employee instances.
        """
        if self.__employee_list == []:
            with open(self.EMPLOYEE_FILE, "r") as employee_file:
                csv_reader = csv.DictReader(employee_file)
                for line in csv_reader:
                    employee = Employee(
                        line["title"],
                        line["name"],
                        line["id"],
                        line["password"])
                    self.__employee_list.append(employee)
        return self.__employee_list

    def set_current_employee(self, employee):
        self.__current_employee = employee

    def get_current_employee(self):
        return self.__current_employee
