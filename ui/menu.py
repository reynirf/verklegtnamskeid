from lib.nocco_list import NoccoList
from lib.color import Color
from ui.frame import Frame
from models.employee import Employee
from models.customer import Customer
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
        self.__current_customer = ""

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
        customer_list = self.nocco_list.choose_one('Choose an action', 
            ['Register customer','Edit customer', 'Find customer','Go back'],
            'action')
        self.handle_answer_from_menu(customer_list['action'], 'customer')
    
    def order(self):
        order_list = self.nocco_list.choose_one("Choose an action",["Register order","Find order","Calculate order", "Go back"], "action")
        self.handle_answer_from_menu(order_list['action'],'order')

    def save_new_order(self):
        self.order_manager.save_new_order()
        print("{}".format(self.color.return_colored("New order registered", 'green')))
        time.sleep(2)
        self.frame.delete_last_lines(1)

    def register_order(self):
        self.frame.delete_last_lines(7)

        self.check_if_valid('ID', self.order_manager.check_ID)

        self.check_if_valid('SSN', self.order_manager.check_ssn)

        self.check_if_valid('Make', self.order_manager.check_make)

        self.check_if_valid('Start date', self.order_manager.check_start_date)

        self.check_if_valid('Ending date', self.order_manager.check_ending_date)

        self.check_if_valid('Pick up time', self.order_manager.check_pick_up_time)

        self.check_if_valid('Returning time', self.order_manager.check_returning_time)

        self.check_if_valid('Pick up location', self.order_manager.check_pick_up_location)

        self.check_if_valid('Return location', self.order_manager.check_return_location)

        self.check_if_valid('Number of seats', self.order_manager.check_number_of_seats)

        self.check_if_valid('Number plate', self.order_manager.check_number_plate)

        self.check_if_valid('Insurance', self.order_manager.check_insurance)
        print()
        register_order_list = self.nocco_list.choose_one("Choose an action",["Save", "Print order",
        "Show all available cars", "Cancel"], "action")
        self.handle_answer_from_menu(register_order_list['action'], 'register_order')


    def check_if_valid(self, to_enter, to_check):
        mistake = 0
        error = "check if valid"
        while error:
            user_input = input("Enter " + to_enter + ': ')
            error = to_check(user_input)
            if error and not mistake:
                self.invalid_input(error)
                mistake = 1
            elif error:
                self.frame.delete_last_lines()
            elif mistake and not error:
                self.frame.delete_last_lines(2)
                print("Enter " + to_enter + ': ' + user_input)

    def register_customer(self):
        self.frame.delete_last_lines(7)

        self.check_if_valid('Name', self.customer_manager.check_name)

        self.check_if_valid('SSN', self.customer_manager.check_ssn)
        
        self.check_if_valid('Birthday', self.customer_manager.check_birthday)

        self.check_if_valid('Phone number', self.customer_manager.check_phone_number)

        self.check_if_valid('Driving License Category', self.customer_manager.check_license)

        self.check_if_valid('Email', self.customer_manager.check_email)

        self.check_if_valid('Credit Card Number', self.customer_manager.check_credit_card)
        
        self.check_if_valid('Home Address', self.customer_manager.check_address)

        print()
        register_customer_list = self.nocco_list.choose_one('Choose an action', 
            ['Save','Cancel'],
            'action')
        self.handle_answer_from_menu(register_customer_list['action'], 'register customer')
    
    def invalid_input(self, message):
        self.frame.delete_last_lines(1)
        print('{}'.format(self.color.return_colored(message, 'red')))

    def save_new_customer(self):
        self.customer_manager.save_new_customer()
        print("{}".format(self.color.return_colored("New customer registered", 'green')))
        time.sleep(2)
        self.frame.delete_last_lines(1)
        
    def find_customer(self):
        find_customer_list = self.nocco_list.choose_one('Choose an action', 
            ['Find customer by Name', 'Find customer by SSN', 'Go back'], 'action')
        self.handle_answer_from_menu(find_customer_list['action'], 'find customer')

    def find_customer_by_name(self):
        name = input("Enter name: ")
        print()
        customer = self.customer_manager.find_customer_by_name(name)
        if customer == None:
            print('{}'.format(self.color.return_colored("Customer not found!", 'red')))
            time.sleep(1.5)
            self.frame.delete_last_lines(4)
            print()
            self.find_customer()
        else:
            for i,person in enumerate(customer):
                print("Customer " + str(i+1) + ": " + person.__str__())
            print()
            if len(customer) == 1:
                self.__current_customer = customer[0]
                found_customer_list = self.nocco_list.choose_one('Choose an action',
                    ['Edit customer', 'Unsubscribe customer', 'Go back'], 'action')
                self.frame.delete_last_lines(2)
                self.handle_answer_from_menu(found_customer_list['action'], 
                    'found customer')
            else:
                print("{}".format(self.color.return_colored("There are multiple customers with that name!", 'red')))
                print()
                found_multiple_customers = self.nocco_list.choose_one('Choose an action',
                    ['Try again', 'Go back'], 'action')
                self.frame.delete_last_lines(len(customer) + 1)
                self.handle_answer_from_menu(found_multiple_customers['action'], 
                    'found multiple customers')
    
    def find_customer_by_ssn(self):
        ssn = input("Enter SSN: ")
        print()
        customer = self.customer_manager.find_customer_by_ssn(ssn)
        if customer == None:
            print('{}'.format(self.color.return_colored("Customer not found", 'red')))
            time.sleep(1.5)
            self.frame.delete_last_lines(4)
            print()
            self.find_customer()
        else:
            self.frame.delete_last_lines(2)
            self.__current_customer = customer
            print("Customer : " + customer.__str__())
            print()
            found_customer_list = self.nocco_list.choose_one('Choose an action',
                    ['Print customer details', 'Edit customer', 'Unsubscribe customer', 'Go back'], 'action')
            self.frame.delete_last_lines(2)
            self.handle_answer_from_menu(found_customer_list['action'], 
                    'found customer') 

    def delete_customer(self):
        self.customer_manager.delete_customer(self.__current_customer)
        print('{}'.format(self.color.return_colored("Customer removed from file", 'red')))

    def save_new_car(self):
        self.vehicle_manager.save_new_car()
        print("{}".format(self.color.return_colored("New car registered!", 'green')))
        time.sleep(2)
        self.frame.delete_last_lines(2)

    def show_all_available_cars(self):
        test_data = [['Toyota', 'Huyndai', 'Ford', 'Reynir', 'Sixarinn'], ['Renault', 'Viddi', 'Peugot', 'Guðrún','Ermir'], ['Nike', 'Subaru', 'Volvo','Bíll','Hilux']]

        col_width = max(len(word) for row in test_data for word in row) + 2 
        for row in test_data:
            print ("".join(word.ljust(col_width) for word in row))

        self.nocco_list.single_list('Go back')


    def cars(self):
        self.frame.delete_last_lines(7)
        car = self.nocco_list.choose_one('Choose an action', ['Register car', 'Find car', 'Show all available cars',
            'Show cars in service', 'Show cars that require maintance', 'Show cars that must be checked',
            'Go back'], 'action')
        self.handle_answer_from_menu(car['action'], 'cars')
    
    def find_cars(self):
        self.frame.delete_last_lines(7)
        find_cars = self.nocco_list.choose_one('Choose an action', ['Find car by number plate', 'Find car by make',
         'Find car by type','Go back'], 'action')
        print()
        self.handle_answer_from_menu(find_cars['action'], 'find car')
    
    def find_cars_by_number_plate(self):
        number_pl = input("Enter number plate: ")
        print()
        cars = self.vehicle_manager.find_car_by_number_plate(number_pl)
        if cars == None:
            print('{}'.format(self.color.return_colored("Car not found!", 'red')))
            time.sleep(2)
            self.frame.delete_last_lines(2)
            self.find_cars()
        else:
            pass
    
    def find_cars_by_number_make(self):
        make = input("Enter make: ")
        print()
        cars = self.vehicle_manager.find_car_by_make(make)
        if cars == None:
            print('{}'.format(self.color.return_colored("Car not found!", 'red')))
            time.sleep(2)
            self.frame.delete_last_lines(2)
            self.find_cars()
        else:
            pass

    def find_cars_by_number_type(self):
        type_of_car = input("Enter type: ")
        print()
        cars = self.vehicle_manager.find_car_by_type(type_of_car)
        if cars == None:
            print('{}'.format(self.color.return_colored("Car not found!", 'red')))
            time.sleep(2)
            self.frame.delete_last_lines(2)
            self.find_cars()
        else:
            pass

    def register_car(self):
        self.frame.delete_last_lines(8)

        self.check_if_valid('Car type', self.vehicle_manager.check_type)

        self.check_if_valid('Make', self.vehicle_manager.check_make)

        self.check_if_valid('Model', self.vehicle_manager.check_model)

        self.check_if_valid('Year', self.vehicle_manager.check_year)

        self.check_if_valid('Car type', self.vehicle_manager.check_type)
    
        self.check_if_valid('Number of seats', self.vehicle_manager.check_number_of_seats)

        self.check_if_valid('Number plate', self.vehicle_manager.check_number_plate)

        self.check_if_valid('Fuel', self.vehicle_manager.check_fuel)

        self.check_if_valid('Driving transmission', self.vehicle_manager.check_driving_transmission)
        print()
        register_car = self.nocco_list.choose_one('Choose an action', 
            ['Save','Cancel'],
            'action')
        self.handle_answer_from_menu(register_car['action'], 'register car')


    def init_menu(self):
            prompt = self.nocco_list.choose_one(
                'Choose an action', 
                ['Order','Customer','Cars', 'Report an error','Log out'],
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

            elif prompt.lower() == 'report an error':
                self.report_error()
                self.init_menu()

            elif prompt.lower() == 'customer':
                self.frame.delete_last_lines(7)
                self.customer()

            elif prompt.lower() == 'cars':
                self.cars()

            elif prompt.lower() == 'order':
                self.frame.delete_last_lines(7)
                self.order()
        
        ######################################################    
        #                      ORDER                         #
        ######################################################

        elif menu_type == 'order':
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(6)
                self.init_menu()
            elif prompt.lower() == 'register order':
                print()
                self.register_order()
            elif prompt.lower() == 'find order':
                pass
            elif prompt.lower() == 'calculate order':
                pass     

        ######################################################    
        #                      CUSTOMER                      #
        ######################################################

        elif menu_type == 'customer':
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(6)
                self.init_menu()
            elif prompt.lower() == 'register customer':
                print()
                self.register_customer()
            elif prompt.lower() == 'edit customer':
                pass
            elif prompt.lower() == 'find customer':
                self.frame.delete_last_lines(6)
                self.find_customer()
        
        ######################################################    
        #                    REGISTER CUSTOMER               #                    
        ######################################################
        elif menu_type == 'register customer':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(13)
                self.save_new_customer()
                # print('\n' * 6)
                self.customer()

            elif prompt.lower() == 'cancel':
                self.frame.delete_last_lines(15)
                self.customer()
        
        ######################################################    
        #                    FIND CUSTOMER                   #                    
        ######################################################
        elif menu_type == 'find customer':
            if prompt.lower() == 'find customer by name':
                self.frame.delete_last_lines(5)
                self.find_customer_by_name()
            elif prompt.lower() == 'find customer by ssn':
                self.frame.delete_last_lines(5)
                self.find_customer_by_ssn()
            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(5)
                self.customer()

        ######################################################    
        #               FOUND MULTIPLE CUSTOMERS             #                    
        ######################################################
        if menu_type == 'found multiple customers':
            if prompt.lower() == 'try again':
                self.frame.delete_last_lines(8)
                self.find_customer()
            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(8)
                self.customer()

        ######################################################    
        #                    FOUND CUSTOMER                  #                    
        ######################################################
        if menu_type == 'found customer':
            if prompt.lower() == 'print customer details':
                customer_details = self.__current_customer.return_details()
                self.frame.delete_last_lines(6)
                for detail, value in customer_details.items():
                    print("{}: {}".format(detail, value))
                self.nocco_list.single_list('Go back')
                self.frame.delete_last_lines(10)
                self.customer()

            elif prompt.lower() == 'edit customer':
                self.frame.delete_last_lines(5)
                pass
            elif prompt.lower() == 'unsubscribe customer':
                self.frame.delete_last_lines(5)
                self.delete_customer()
            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(5)
                self.find_customer()

        ######################################################    
        #                       CARS                         #                    
        ######################################################
        elif menu_type == 'cars':
            if prompt.lower() == 'register car':
                self.frame.delete_last_lines(1)
                self.register_car()
                self.cars()

            if prompt.lower() == 'find car':
                self.frame.delete_last_lines(1)
                self.find_cars()
                self.cars()

            elif prompt.lower() == 'show all available cars':
                self.frame.delete_last_lines(9)
                self.show_all_available_cars()
                print()
                print()
                self.cars()

            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(9)
                self.init_menu()

        ########################################################
        #                REGISTER NEW ORDER                    #
        ########################################################
        elif menu_type == 'register_order':
            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(19)
                self.order()

            elif prompt.lower() == 'show all available cars':
                self.frame.delete_last_lines(19)
                self.show_all_available_cars()
                self.frame.delete_last_lines(5)
                self.order()

            elif prompt.lower() == 'save':
                self.frame.delete_last_lines(14)
                self.frame.delete_last_lines(5)
                self.save_new_order()
                self.order()
                
        ######################################################    
        #                    FIND CAR                        #                    
        ######################################################
        elif menu_type == 'find car':
            if prompt.lower() == 'find car by number plate':
                self.frame.delete_last_lines(5)
                self.find_cars_by_number_plate()
            elif prompt.lower() == 'find car by make':
                self.frame.delete_last_lines(5)
                self.find_cars_by_number_make()
            elif prompt.lower() == 'find car by type':
                self.frame.delete_last_lines(5)
                self.find_cars_by_number_type()
            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(5)
                # It goes in cars menu if clicking go back!
                self.cars()

        ######################################################    
        #                    FOUND CAR                       #                    
        ######################################################
        elif menu_type == 'found car':
            if prompt.lower() == 'edit car':
                self.frame.delete_last_lines(5)
                # TODO edit car
                pass
            elif prompt.lower() == 'remove car':
                # TODO remove car
                pass
            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(5)
                self.find_cars()


        ######################################################    
        #                    REGISTER CAR                    #                    
        ######################################################
        elif menu_type == 'register car':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(16)
                self.save_new_car()
                print("\n" * 7)
                self.cars()
            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(10)
                self.cars()
