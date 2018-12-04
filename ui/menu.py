import os.path
from lib.nocco_list import NoccoList
from lib.color import Color
from ui.frame import Frame
from models.employee import Employee
import csv
import time
import getpass
from service.employee_manager import EmployeeManager


class Menu:
    def __init__(self):
        self.nocco_list = NoccoList()
        self.color = Color()
        self.frame = Frame()
        self.employee_manager = EmployeeManager()

    def get_employees(self):
        employee_list = self.employee_manager.get_employee_list()
        return_string = ""
        for employee in employee_list:
            return_string += (print(employee) + "/n")
        return return_string

    def authenticate_v2(self):
        print()
        print()
        logged_in = False
        while logged_in == False:
            employee_id = input('Enter your ID: ')
            employee_password = input('Enter password: ')
            response = self.employee_manager.authenticate(employee_id, employee_password)
            if type(response) == Employee:
                self.frame.delete_last_lines(3)
                return response
            else:
                self.frame.delete_last_lines(3)
                self.color.print_colored(response, 'red')

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

    def logout(self, employee):
        self.frame.delete_last_lines(9)
        print('{} has been logged out'.format(
            self.color.return_colored(employee.get_name(), 'red'
        )))
        time.sleep(2)
        self.frame.delete_last_lines(3)
        return self.authenticate_v2()

    def report_error(self):
        self.frame.delete_last_lines(7)
        print('Contact your manager to report an error')
        self.nocco_list.single_list('Go back')
        self.frame.delete_last_lines(3)
    
    def customer(self,employee):
        self.frame.delete_last_lines(7)
        customer_list = self.nocco_list.choose_one('Choose an action', 
            ['Customer','Register customer','Edit list of customer', 'Find customer','Go back'],
            'action')
        self.handle_answer_from_menu(customer_list['action'], employee, 'customer')

    def register_customer(self,employee):
        self.frame.delete_last_lines(7)
        name = input("Enter Name: ")
        ssn = input("Enter SSN: ")
        birthday = input("Enter Birthday: ")
        phone_number = input("Enter Phone number: ")
        driving_license_category = input("Enter Driving Licence Category: ")
        email = input("Enter Email: ")
        credit_card = input("Enter Credit Card Number: ")
        home_address = input("Enter Home Address: ")
        print()
        register_customer_list = self.nocco_list.choose_one('Choose an action', 
            ['Save','Print information','Cancel'],
            'action')
        self.handle_answer_from_menu(register_customer_list['action'], employee, 'register_customer')

        loller = self.nocco_list.choose_one('Choose an action', 
            ['Customer','Register customer','Edit list of customer', 'Find customer','Go back'],
            'action')
        self.handle_answer_from_menu(loller['action'], employee, 'register_customer')
            
    def cars(self, employee):
        self.frame.delete_last_lines(7)
        car = self.nocco_list.choose_one('Choose an action', ['Register car', 'Find car', 'Show all available cars',
            'Show cars in service', 'Show cars that require maintance', 'Show cars that must be checked',
            'Go back'], 'action')
        self.handle_answer_from_menu(car['action'], employee, 'cars')    

    def handle_answer_from_menu(self, prompt, employee, menu_type):

        ######################################################
        #                      MAIN MENU                     #                                                                                
        ######################################################
        if menu_type == 'main_menu':
            if prompt.lower() == 'logout':
                #logout and return the next user who logs into the system
                new_employee = self.logout(employee) 
                self.init_menu(new_employee)
            if prompt.lower() == 'report an error':
                self.report_error()
                self.init_menu(employee)
            if prompt.lower() == 'customer':
                self.customer(employee)
            if prompt.lower() == 'cars':
                self.cars(employee)

        ######################################################    
        #                      CUSTOMER                      #
        ######################################################

        if menu_type == 'customer':
            if prompt.lower() == 'customer':
                self.customer(employee)
                self.init_menu(employee)
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(7)
                self.init_menu(employee)
            if prompt.lower() == 'register customer':
                self.register_customer(employee)
                self.init_menu(employee)
        
        ######################################################    
        #                    REGISTER CUSTOMER               #                    
        ######################################################
        if menu_type == 'register_customer':
            if prompt.lower() == 'save':
                pass
            if prompt.lower() == 'print information':
                pass
            if prompt.lower() == 'cancel':
                pass
        
        ######################################################    
        #                       CARS                          #                    
        ######################################################
        if menu_type == 'cars':
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(9)
                self.init_menu(employee)

    def init_menu(self, employee):
            prompt = self.nocco_list.choose_one(
                'Choose an action', 
                ['Order','Customer','Cars', 'Report an error','Logout'],
                'action'
            )
            self.handle_answer_from_menu(prompt['action'], employee, 'main_menu')



