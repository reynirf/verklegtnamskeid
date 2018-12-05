from lib.nocco_list import NoccoList
from lib.color import Color
from ui.frame import Frame
from models.employee import Employee
from service.employee_manager import EmployeeManager
from service.customer_manager import CustomerManager
from service.vehicle_manager import VehicleManager
import csv
import time
import getpass
import os.path



class Menu:
    def __init__(self):
        self.nocco_list = NoccoList()
        self.color = Color()
        self.frame = Frame()
        self.employee_manager = EmployeeManager()
        self.customer_manager = CustomerManager()
        self.vehicle_manager = VehicleManager()

    def get_employees(self):
        employee_list = self.employee_manager.get_employee_list()
        for employee in employee_list:
            print(employee)

    def authenticate_v2(self):
        print()
        print()
        logged_in = False
        while logged_in == False:
            employee_id = input('Enter your ID: ')
            employee_password = getpass.getpass('Enter password: ')
            response = self.employee_manager.authenticate(employee_id, employee_password)
            if type(response) == Employee:
                print()
                if self.employee_manager.has_failed():
                    self.frame.delete_last_lines(4)
                    print('\n' * 3)
                self.introduce_employee(response)
                print()
                logged_in = True
            else:
                self.frame.delete_last_lines(3)
                self.color.print_colored(response, 'red')

    def introduce_employee(self, employee):
        self.frame.delete_last_lines(3)
        print(employee)

    def logout(self):
        self.frame.delete_last_lines(9)
        employee = self.employee_manager.get_current_employee()
        print('{} has been logged out'.format(
            self.color.return_colored(employee.get_name(), 'red'
        )))
        time.sleep(2)
        self.frame.delete_last_lines(3)
        self.authenticate_v2()

    def report_error(self):
        self.frame.delete_last_lines(7)
        print('Contact your manager to report an error')
        self.nocco_list.single_list('Go back')
        self.frame.delete_last_lines(3)
    
    def customer(self):
        self.frame.delete_last_lines(7)
        customer_list = self.nocco_list.choose_one('Choose an action', 
            ['Customer','Register customer','Edit list of customer', 'Find customer','Go back'],
            'action')
        self.handle_answer_from_menu(customer_list['action'], 'customer')
    
    def order(self):
        self.frame.delete_last_lines(7)
        order_list = self.nocco_list.choose_one("Choose an action",["Register order","Find order","Calculate order", "Go back"], "action")
        self.handle_answer_from_menu(order_list['action'],'order')
   
    def register_order(self):
        self.frame.delete_last_lines(7)
        id = input("Id of order: ")
        customer = input("Enter Customer: ")
        employee = input("Enter employee: ")
        car = input("Enter car: ")
        start_date = input("Enter start date: ")
        ending_date = input("Enter ending date: ")
        pick_up_location = input("Enter pick up location: ")
        return_location = input("Enter return location: ")
        insurance = input("Enter insurance: ")
        print()
        register_order_list = self.nocco_list.choose_one("Choose an action",["Save", "Print order", "Cancel"], "action")
        self.handle_answer_from_menu(register_order_list['action'], 'register_order')

    def register_customer(self):
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
        self.handle_answer_from_menu(register_customer_list['action'], 'register_customer')
            
    def cars(self):
        self.frame.delete_last_lines(7)
        car = self.nocco_list.choose_one('Choose an action', ['Register car', 'Find car', 'Show all available cars',
            'Show cars in service', 'Show cars that require maintance', 'Show cars that must be checked',
            'Go back'], 'action')
        self.handle_answer_from_menu(car['action'], 'cars')    

    def init_menu(self):
            prompt = self.nocco_list.choose_one(
                'Choose an action', 
                ['Order','Customer','Cars', 'Report an error','Logout'],
                'action'
            )
            self.handle_answer_from_menu(prompt['action'], 'main_menu')

    def handle_answer_from_menu(self, prompt, menu_type):

        ######################################################
        #                      MAIN MENU                     #                                                                                
        ######################################################
        if menu_type == 'main_menu':
            if prompt.lower() == 'logout':
                self.logout() 
                self.init_menu()
            if prompt.lower() == 'report an error':
                self.report_error()
                self.init_menu()
            if prompt.lower() == 'customer':
                self.customer()
            if prompt.lower() == 'cars':
                self.cars()
            if prompt.lower() == 'order':
                self.order()
        
        ######################################################    
        #                      ORDER                      #
        ######################################################

        if menu_type == 'order':
            if prompt.lower() == 'order':
                self.order()
                self.init_menu()
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(7)
                self.init_menu()
            if prompt.lower() == 'register order':
                self.register_order()
                self.init_menu()
        

        ######################################################    
        #                      CUSTOMER                      #
        ######################################################

        if menu_type == 'customer':
            if prompt.lower() == 'customer':
                self.customer()
                self.init_menu()
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(7)
                self.init_menu()
            if prompt.lower() == 'register customer':
                self.register_customer()
                self.init_menu()
        
        ######################################################    
        #                    REGISTER CUSTOMER               #                    
        ######################################################
        if menu_type == 'register_customer':
            if prompt.lower() == 'save':
                pass
            if prompt.lower() == 'print information':
                pass
            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(14)
        
        ######################################################    
        #                       CARS                          #                    
        ######################################################
        if menu_type == 'cars':
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(9)
                self.init_menu()



