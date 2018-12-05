from lib.nocco_list import NoccoList
from lib.color import Color
from ui.frame import Frame
from models.employee import Employee
from service.employee_manager import EmployeeManager
from service.customer_manager import CustomerManager
from service.vehicle_manager import VehicleManager
from service.order_manager import OrderManager
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
        self.order_manager = OrderManager()

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
            ['Register customer','Edit list of customer', 'Find customer','Go back'],
            'action')
        self.handle_answer_from_menu(customer_list['action'], 'customer')
    
    def order(self):
        self.frame.delete_last_lines(7)
        order_list = self.nocco_list.choose_one("Choose an action",["Register order","Find order","Calculate order", "Go back"], "action")
        self.handle_answer_from_menu(order_list['action'],'order')

    def save_new_order(self):
        self.order_manager.save_new_order()
        print("{}".format(self.color.return_colored("New order registered", 'green')))
        time.sleep(2)
        self.frame.delete_last_lines(1)

    def register_order(self):
        self.frame.delete_last_lines(7)
        ID = input("Id of order: ")
        self.order_manager.check_id(ID)
        ssn = input("Enter Customer SSN: ")
        self.order_manager.check_ssn(ssn)
        car = input("Enter car: ")
        self.order_manager.check_car(car)
        start_date = input("Enter start date: ")
        self.order_manager.check_start_date(start_date)
        ending_date = input("Enter end date: ")
        self.order_manager.check_ending_date(ending_date)
        pick_up_time = input("Enter pick up time: ")
        self.order_manager.check_pick_up_time(pick_up_time)
        returning_time = input("Enter returning time: ")
        self.order_manager.check_returning_time(returning_time)
        pick_up_location = input("Enter pick up location: ")
        self.order_manager.check_pick_up_location(pick_up_location)
        return_location = input("Enter return location: ")
        self.order_manager.check_return_location(return_location)
        number_of_seats = input("Enter number of seats: ")
        self.order_manager.check_number_of_seats(number_of_seats)
        number_plate = input("Enter Number Plate: ")
        self.order_manager.check_number_plate(number_plate)
        insurance = input("Enter insurance: ")
        self.order_manager.check_insurance(insurance)
        print()
        register_order_list = self.nocco_list.choose_one("Choose an action",["Save", "Print order",
        "Show all available cars", "Cancel"], "action")
        self.handle_answer_from_menu(register_order_list['action'], 'register_order')

    def register_customer(self):
        self.frame.delete_last_lines(7)
        
        name_check = "check if valid"
        while type(name_check) == str:
            name = input("Enter Name: ")
            name_check = self.customer_manager.check_name(name)
            if type(name_check) == str:
                self.invalid_input(name_check)
        
        ssn_check = "check if valid"
        while type(ssn_check) == str:
            ssn = input("Enter SSN: ")
            ssn_check = self.customer_manager.check_ssn(ssn)
            if type(ssn_check) == str:
                self.invalid_input(ssn_check)
        
        birthday_check = "check if valid"
        while type(birthday_check) == str:
            birthday = input("Enter Birthday: ")
            birthday_check = self.customer_manager.check_birthday(birthday)
            if type(birthday_check) == str:
                self.invalid_input(birthday_check)
        
        phone_check = "check if valid"
        while type(phone_check) == str:
            phone_number = input("Enter Phone number: ")
            phone_check = self.customer_manager.check_phone_number(phone_number)
            if type(phone_check) == str:
                self.invalid_input(phone_check)

        license_check = "check if valid"
        while type(license_check) == str:
            driving_license_category = input("Enter Driving License Category: ")
            license_check = self.customer_manager.check_license(driving_license_category)
            if type(license_check) == str:
                self.invalid_input(license_check)
        
        email_check = "check if valid"
        while type(email_check) == str:
            email = input("Enter Email: ")
            email_check = self.customer_manager.check_email(email)
            if type(email_check) == str:
                self.invalid_input(email_check)
        
        credit_card_check = "check if valid"
        while type(credit_card_check) == str:
            credit_card = input("Enter Credit Card Number: ")
            credit_card_check = self.customer_manager.check_credit_card(credit_card)
            if type(credit_card_check) == str:
                self.invalid_input(credit_card_check)
        
        home_address = input("Enter Home Address: ")
        self.customer_manager.check_address(home_address)
        print()
        register_customer_list = self.nocco_list.choose_one('Choose an action', 
            ['Save','Print information','Cancel'],
            'action')
        self.handle_answer_from_menu(register_customer_list['action'], 'register_customer')
    
    def invalid_input(self, message):
        self.frame.delete_last_lines(1)
        print('{}'.format(self.color.return_colored(message, 'red')))

    def save_new_customer(self):
        self.customer_manager.save_new_customer()
        print("{}".format(self.color.return_colored("New customer registered", 'green')))
        time.sleep(2)
        self.frame.delete_last_lines(1)
    def save_new_car(self):
        self.vehicle_manager.save_new_car()
        print("{}".format(self.color.return_colored("New customer registered", 'green')))
        time.sleep(2)
        self.frame.delete_last_lines(2)

    def cars(self):
        self.frame.delete_last_lines(7)
        car = self.nocco_list.choose_one('Choose an action', ['Register car', 'Find car', 'Show all available cars',
            'Show cars in service', 'Show cars that require maintance', 'Show cars that must be checked',
            'Go back'], 'action')
        self.handle_answer_from_menu(car['action'], 'cars')

    def register_car(self):
        self.frame.delete_last_lines(7)
        car_type = input("Enter Type: ")
        self.vehicle_manager.check_type(car_type)
        make = input("Enter Make: ")
        self.vehicle_manager.check_make(make)
        model = input("Enter Model: ")
        self.vehicle_manager.check_model(model)
        year = input("Enter Year: ")
        self.vehicle_manager.check_year(year)
        number_of_seats = input("Enter Number: ")
        self.vehicle_manager.check_number_of_seats(number_of_seats)
        number_plate = input("Enter Number Plate: ")
        self.vehicle_manager.check_number_plate(number_plate)
        fuel = input("Enter Fuel: ")
        self.vehicle_manager.check_fuel(fuel)
        driving_transmission = input("Enter Driving Transmission: ")
        self.vehicle_manager.check_driving_transmission(driving_transmission)
        print()
        register_car = self.nocco_list.choose_one('Choose an action', 
            ['Save','Print information','Cancel'],
            'action')
        self.handle_answer_from_menu(register_car['action'], 'cars')


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
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(6)
                self.init_menu()
            if prompt.lower() == 'register order':
                print()
                self.register_order()
                self.init_menu()
            if prompt.lower() == 'find order':
                pass
            if prompt.lower() == 'calculate order':
                pass     

        ######################################################    
        #                      CUSTOMER                      #
        ######################################################

        if menu_type == 'customer':
            if prompt.lower() == 'customer':
                self.customer()
                self.init_menu()
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(6)
                self.init_menu()
            if prompt.lower() == 'register customer':
                print()
                self.register_customer()
                self.init_menu()
        
        ######################################################    
        #                    REGISTER CUSTOMER               #                    
        ######################################################
        if menu_type == 'register_customer':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(14)
                self.save_new_customer()
                print('\n' * 6)
                self.customer()
            if prompt.lower() == 'print information':
                pass
            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(7)
                self.customer()
        
        ######################################################    
        #                       CARS                          #                    
        ######################################################
        if menu_type == 'cars':
            if prompt.lower() == 'register car':
                self.frame.delete_last_lines(1)
                self.register_car()
                self.cars()
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(14)
                self.save_new_car()
                print("\n" * 6)
                self.cars()

            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(9)
                self.init_menu()

        ########################################################
        #                Register new order                    #
        ########################################################
        if menu_type == 'register_order':
            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(8)
                self.order()
            if prompt.lower() == 'show all available cars':
                pass
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(14)
                self.save_new_order()
                print("\n" * 6)
                self.order


