from models.employee import Employee
import csv

class EmployeeRepo:

    EMPLOYEE_FILE = "./data/employees.csv"

    def __init__(self):
        self.employee_list = []
        self.current_employee = ""
    
    def get_employee_list(self):
        if self.employee_list == []:
            with open(self.EMPLOYEE_FILE, 'r') as employee_file:
                csv_reader = csv.DictReader(employee_file)
                for line in csv_reader:
                    employee = Employee(line['name'], line['id'], line['password'])
                    self.employee_list.append(employee)
        return self.employee_list

