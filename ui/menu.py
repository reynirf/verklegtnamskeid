from lib.nocco_list import NoccoList
from lib.color import Color
from ui.frame import Frame
from models.employee import Employee
import csv
import time
import getpass

class Menu:
    def __init__(self):
        self.nocco_list = NoccoList()
        self.color = Color()
        self.frame = Frame()

    def get_employees(self):
        with open('data/employees.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            employees = {}
            for i,employee in enumerate(csv_reader):
                if i != 0:
                    e_id = employee[0]
                    employees[e_id] = {
                        'name': employee[1],
                        'password': employee[2]
                    } 
            return employees

    def authenticate(self, employees, has_failed=0):
        try:
            employee_id = input('Enter your ID: ')
            employee_password = getpass.getpass('Enter password: ')
            #test to see if the employee_id exists. 
            # If it doesn't exist, it will raise a KeyError
            employees[employee_id] 
            
            if employee_password != employees[employee_id]['password']:
                raise ValueError
            return (employees[employee_id],employee_id),has_failed
        except KeyError:
            has_failed = True
            self.frame.delete_last_lines(3)
            self.color.print_colored('Invalid ID: ' + employee_id, 'red')
            return self.authenticate(employees,has_failed)
        except ValueError:
            has_failed = True
            self.frame.delete_last_lines(3)
            self.color.print_colored('Wrong password', 'red')
            return self.authenticate(employees,has_failed)

    def initialize_employee(self, employee):
        info = employee[0]
        employee_id = employee[1]
        password = info['password']
        name = info['name']
        employee = Employee(name,employee_id,password)
        return employee

    def introduce_employee(self, employee):
        self.frame.delete_last_lines(3)
        print(employee)

    def authenticate_process(self, employees):
        print() #ekki remove'a
        print()
        employee,has_failed = self.authenticate(employees)
        print()
        employee = self.initialize_employee(employee)
        if has_failed:
            self.frame.delete_last_lines(4)
            print()
            print()
            print()
            print()
        self.introduce_employee(employee)
        print()

        return employee

    def logout(self, employee, employees):
        self.frame.delete_last_lines(9)
        print('{} has been logged out'.format(
            self.color.return_colored(employee.get_name(), 'red'
        )))
        time.sleep(2)
        self.frame.delete_last_lines(3)
        return self.authenticate_process(employees)

    def report_error(self):
        self.frame.delete_last_lines(7)
        print('Contact your manager to report an error')
        self.nocco_list.single_list('Go back')
        self.frame.delete_last_lines(3)

    def handle_answer_from_menu(self, prompt, employee, employees):
        if prompt.lower() == 'logout':
            #logout and return the next user who logs into the system
            new_employee = self.logout(employee, employees) 
            self.init_menu(new_employee, employees)
        if prompt.lower() == 'report an error':
            self.report_error()
            self.init_menu(employee, employees)

    def init_menu(self, employee, employees):
        prompt = self.nocco_list.choose_one(
            'Choose an action', 
            ['Order','Customer','Cars', 'Report an error','Logout'],
            'action'
        )
        self.handle_answer_from_menu(prompt['action'], employee, employees)
