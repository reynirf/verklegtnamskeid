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
        self.__current_vehicle = ""

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

    def signout(self):
        self.frame.delete_last_lines(9)
        employee = self.employee_manager.get_current_employee()
        print('{} has been logged out'.format(
            self.color.return_colored(employee.get_name(), 'red'
        )))
        time.sleep(1.5)
        self.frame.delete_last_lines(3)
        self.authenticate_v2()

    def report_error(self):
        self.frame.delete_last_lines(7)
        print('Contact your manager to report an error')
        self.nocco_list.single_list('Go back')
        self.frame.delete_last_lines(3)
    
    def customer(self):
        customer = self.nocco_list.choose_one('Choose an action', 
            ['Register customer', 'Find customer','Go back'],
            'action')
        self.handle_answer_from_menu(customer['action'], 'customer')
    
    def order(self):
        order_list = self.nocco_list.choose_one("Choose an action",["Register order","Find order", "Go back"], "action")
        self.handle_answer_from_menu(order_list['action'],'order')
    
    def calculate_order(self):
        #self.order_manager.calculate_order()
        self.frame.delete_last_lines(2)
        print(self.order_manager.calculate_order())
        print()
        calculate_order_list = self.nocco_list.choose_one("Choose an action",["Go back"], "action")
        self.handle_answer_from_menu(calculate_order_list['action'],'order')

    
    def find_order_by_id(self):
        ID = input("Enter ID: ")
        print()
        order = self.order_manager.find_order_by_id(ID)
        if order == None:
            print('{}'.format(self.color.return_colored("Order not found!", 'red')))
            time.sleep(1.5)
            self.frame.delete_last_lines(2)
            self.find_order()
        else:
            for i,person in enumerate(order):
                print("Order " + str(i+1) + ": " + person.__str__())
            print()
            if len(order) == 1:
                found_order_list = self.nocco_list.choose_one('Choose an action',
                    ['Edit order', 'Unsubscribe order', 'Go back'], 'action')
                self.frame.delete_last_lines(2)
                self.handle_answer_from_menu(found_order_list['action'], 
                    'found order')
            else:
                print("{}".format(self.color.return_colored("There are multiple orders with that ID!", 'red')))
                print()
                found_multiple_orders = self.nocco_list.choose_one('Choose an action',
                    ['Try again', 'Go back'], 'action')
                self.frame.delete_last_lines(len(order) + 1)
                self.handle_answer_from_menu(found_multiple_orders['action'], 
                    'found multiple orders')
    
    def find_order_by_ssn(self):
        ssn = input("Enter SSN: ")
        print()
        order = self.order_manager.find_order_by_ssn(ssn)
        if order == None:
            print('{}'.format(self.color.return_colored("Order not found", 'red')))
            time.sleep(1.5)
            self.frame.delete_last_lines(3)
            self.find_order()
        else:
            self.frame.delete_last_lines(2)
            print("Order : " + order.__str__())
            print()
            found_order_list = self.nocco_list.choose_one('Choose an action',
                    ['Edit order', 'Delete order', 'Go back'], 'action')
            self.frame.delete_last_lines(2)
            self.handle_answer_from_menu(found_order_list['action'], 
                    'found order') 

    def find_order(self):
        find_order_list = self.nocco_list.choose_one('Choose an action', 
            ['Find order by ID', 'Find order by SSN', 'Go back'], 'action')
        self.handle_answer_from_menu(find_order_list['action'], 'find order')

    def save_new_order(self):
        self.order_manager.save_new_order()
        print("{}".format(self.color.return_colored("New order registered", 'green')))
        time.sleep(1.5)
        self.frame.delete_last_lines(1)
        dates, vehicle = self.order_manager.get_order_dates()
        self.vehicle_manager.save_order_dates(dates, vehicle)

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

        self.check_if_valid('Type of vehicle', self.order_manager.check_type_of_vehicle)

        
        print()
        register_order_list = self.nocco_list.choose_one("Choose an action",["Save", "Calculate order" 
        , "Print order", "Show all available cars", "Cancel"], "action")
        self.handle_answer_from_menu(register_order_list['action'], 'register_order')


    def check_if_valid(self, to_enter, to_check, editing = False, current_value = ''):
        mistake = 0
        error = "check if valid"
        while error:
            if not editing and not current_value:
                user_input = input("Enter " + to_enter + ": ")
            else:
                user_input = input("Enter " + to_enter + " [" + current_value + "]: ")
            error = to_check(user_input, editing, current_value)
            if editing and current_value and not error:
                if mistake: 
                    self.frame.delete_last_lines(2)
                else:
                    self.frame.delete_last_lines()
                if user_input != '':
                    print("Enter " + to_enter + " [" + current_value + "]: " + user_input)
                else:
                    print("Enter " + to_enter + " [" + current_value + "]: " + current_value)
            elif error and not mistake:
                self.invalid_input(error)
                mistake = 1
            elif error:
                self.frame.delete_last_lines()
            elif mistake and not error:
                self.frame.delete_last_lines(2)
                print("Enter " + to_enter + ": " + user_input)

    def register_customer(self):
        self.frame.delete_last_lines(6)

        self.check_if_valid('Name', self.customer_manager.check_name)

        self.check_if_valid('SSN', self.customer_manager.check_ssn)
        
        self.check_if_valid('Birthday', self.customer_manager.check_birthday)

        self.check_if_valid('Phone number', self.customer_manager.check_phone_number)

        self.check_if_valid('Driver license category', self.customer_manager.check_license)

        self.check_if_valid('Email address', self.customer_manager.check_email)

        self.check_if_valid('Credit card number', self.customer_manager.check_credit_card)
        
        self.check_if_valid('Home address', self.customer_manager.check_address)

        print()
        register_customer = self.nocco_list.choose_one('Choose an action', 
            ['Save','Cancel'],
            'action')
        self.handle_answer_from_menu(register_customer['action'], 'register customer')
    
    def edit_customer(self):
        customer = self.__current_customer.return_details()
        print('{}\n'.format(self.color.return_colored('Leave input empty to keep the value the same', 'green')))

        self.check_if_valid('Name', self.customer_manager.check_name, True, customer['Name'])

        self.check_if_valid('SSN', self.customer_manager.check_ssn, True, customer['SSN'])
        
        self.check_if_valid('Birthday', self.customer_manager.check_birthday, True, customer['Birthday'])

        self.check_if_valid('Phone number', self.customer_manager.check_phone_number, True, customer['Phone number'])

        self.check_if_valid('Driver license category', self.customer_manager.check_license, True, customer['Driver license category'])

        self.check_if_valid('Email address', self.customer_manager.check_email, True, customer['Email address'])

        self.check_if_valid('Credit card number', self.customer_manager.check_credit_card, True, customer['Credit card number'])
        
        self.check_if_valid('Home address', self.customer_manager.check_address, True, customer['Home address'])

        print()
        save_edited_customer = self.nocco_list.choose_one('Choose an action', 
            ['Save','Cancel'],
            'action')
        self.handle_answer_from_menu(save_edited_customer['action'], 'save edited customer')

    def invalid_input(self, message):
        self.frame.delete_last_lines(1)
        print('{}'.format(self.color.return_colored(message, 'red')))

    def save_new_customer(self):
        self.customer_manager.save_new_customer()
        print("{}".format(self.color.return_colored("New customer registered", 'green')))
        time.sleep(1.5)
        self.frame.delete_last_lines(1)
        
    def save_edited_customer(self):
        self.customer_manager.delete_customer(self.__current_customer)
        self.customer_manager.save_new_customer()
        print("{}".format(self.color.return_colored("Customer updated", 'green')))
        time.sleep(1.5)
        self.frame.delete_last_lines(1)

    def find_customer(self):
        find_customer = self.nocco_list.choose_one('Choose an action', 
            ['Find customer by Name', 'Find customer by SSN', 'Go back'], 'action')
        self.handle_answer_from_menu(find_customer['action'], 'find customer')

    def found_customer(self):
        found_customer = self.nocco_list.choose_one('Choose an action',
            ['Print customer details', 'Edit customer', 'Unsubscribe customer', 'Go back'], 'action')
        self.frame.delete_last_lines(2)
        self.handle_answer_from_menu(found_customer['action'], 'found customer')

    def find_customer_by_name(self):
        name = input("Enter name: ")
        print()
        customers = self.customer_manager.find_customer_by_name(name)
        if customers == None:
            print('{}'.format(self.color.return_colored("Customer not found!", 'red')))
            time.sleep(1.5)
            self.frame.delete_last_lines(4)
            print()
            self.find_customer()
        else:
            self.frame.delete_last_lines(2)
            if len(customers) == 1:
                self.__current_customer = customers[0]
                self.found_customer()
            else:
                print("{}".format(self.color.return_colored("There are multiple customers with that name!", 'red')))
                print()
                printable_customers = ['{} | {}-{}'.format(customer.__str__(), customer.get_ssn()[:6], customer.get_ssn()[6:]) for customer in customers]

                printable_customers.append('Go back')
                
                found_multiple_customers = self.nocco_list.choose_one('Choose customer',
                    printable_customers, 'customer', True)

                self.handle_answer_from_menu((found_multiple_customers, customers), 
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
            print("Customer: " + customer.__str__())
            print()
            self.found_customer()

    def delete_customer(self):
        self.customer_manager.delete_customer(self.__current_customer)
        self.frame.delete_last_lines()
        print('{}'.format(self.color.return_colored("Customer removed from file", 'red')))
        time.sleep(1.5)
        self.frame.delete_last_lines()
        self.customer()

    def save_new_car(self):
        self.vehicle_manager.save_new_car()
        print("{}".format(self.color.return_colored("New car registered!", 'green')))
        time.sleep(1.5)
        self.frame.delete_last_lines(2)

    def show_all_available_cars(self):
        test_data = [['Toyota', 'Huyndai', 'Ford', 'Reynir', 'Sixarinn'], ['Renault', 'Viddi', 'Peugot', 'Guðrún','Ermir'], ['Nike', 'Subaru', 'Volvo','Bíll','Hilux']]

        col_width = max(len(word) for row in test_data for word in row) + 2 
        for row in test_data:
            print ("".join(word.ljust(col_width) for word in row))

        self.nocco_list.single_list('Go back')
    
    def show_cars_in_service(self):
        test_data = [['Toyota', 'Huyndai', 'Ford', 'Reynir', 'Sixarinn'], ['Renault', 'Viddi', 'Peugot', 'Guðrún','Ermir'], ['Nike', 'Subaru', 'Volvo','Bíll','Hilux']]

        col_width = max(len(word) for row in test_data for word in row) + 2 
        for row in test_data:
            print ("".join(word.ljust(col_width) for word in row))

        self.nocco_list.single_list('Go back')
    
    def show_cars_that_require_maintenance(self):
        test_data = [['Toyota', 'Huyndai', 'Ford', 'Reynir', 'Sixarinn'], ['Renault', 'Viddi', 'Peugot', 'Guðrún','Ermir'], ['Nike', 'Subaru', 'Volvo','Bíll','Hilux']]

        col_width = max(len(word) for row in test_data for word in row) + 2 
        for row in test_data:
            print ("".join(word.ljust(col_width) for word in row))

        self.nocco_list.single_list('Go back')
    
    def show_that_must_be_checked(self):
        test_data = [['Toyota', 'Huyndai', 'Ford', 'Reynir', 'Sixarinn'], ['Renault', 'Viddi', 'Peugot', 'Guðrún','Ermir'], ['Nike', 'Subaru', 'Volvo','Bíll','Hilux']]

        col_width = max(len(word) for row in test_data for word in row) + 2 
        for row in test_data:
            print ("".join(word.ljust(col_width) for word in row))

        self.nocco_list.single_list('Go back')


    def cars(self):
        self.frame.delete_last_lines(7)
        car = self.nocco_list.choose_one('Choose an action', ['Register car', 'Find car', 'Show all available cars',
            'Show cars in service', 'Show cars that require maintenance', 'Show cars that must be checked',
            'Go back'], 'action')
        self.handle_answer_from_menu(car['action'], 'cars')
    
    def find_cars(self):
        find_cars = self.nocco_list.choose_one('Choose an action', ['Find car by number plate', 'Find car by make',
        'Find car by type','Go back'], 'action')
        print()
        self.handle_answer_from_menu(find_cars['action'], 'find car')
    
    def find_cars_by_number_plate(self):
        number_pl = input("Enter number plate: ")
        print()
        car = self.vehicle_manager.find_car_by_number_plate(number_pl)
        if car == None:
            print('{}'.format(self.color.return_colored("Car not found!", 'red')))
            self.frame.delete_last_lines(3)
            time.sleep(1.5)
            self.find_cars()
        else:
            print("Car: "+ car.get_licence())
            print()
            self.__current_vehicle = car
            found_cars_list = self.nocco_list.choose_one("Choose an action",["Edit car", "Remove car", "Go back"],"action") 
            self.frame.delete_last_lines(2)
            self.handle_answer_from_menu(found_cars_list['action'],
            'found car')
    
    def find_cars_by_make(self):
        make = input("Enter make: ")
        print()
        cars = self.vehicle_manager.find_car_by_make(make)
        if cars == None:
            print('{}'.format(self.color.return_colored("Car not found!", 'red')))
            time.sleep(1.5)
            self.frame.delete_last_lines(3)
            self.find_cars()
        else:
            for i,car in enumerate(cars):
                print("Car "+ str(i+1) +": "+ car.get_make())
                time.sleep(1.5)
                # TODO we need to figure out how to handle this
            print()

    def find_cars_by_type(self):
        type_of_car = input("Enter type: ")
        print()
        cars = self.vehicle_manager.find_car_by_type(type_of_car)
        if cars == None:
            print('{}'.format(self.color.return_colored("Car not found!", 'red')))
            time.sleep(1.5)
            self.frame.delete_last_lines(3)
            self.find_cars()
        else:
            for i,car in enumerate(cars):
                print("Car "+ str(i+1) +": "+ car.get_licence())
                # time.sleep(1.5)
            print()     
                # this does not work properly, because we need to handle
                # even when there are more than one car.
            if len(cars) == 1:
                self.__current_vehicle = cars
                # TODO we need to figure out how to handle this
                found_cars_list = self.nocco_list.choose_one("Choose an action",
                ["Edit car","Remove car", "Go back"], "action")
                self.frame.delete_last_lines(2)
                self.handle_answer_from_menu(found_cars_list['action'],'found car')
    
    def delete_vehicle(self):
        self.vehicle_manager.delete_vehicle(self.__current_vehicle)
        self.frame.delete_last_lines(1)
        print('{}'.format(self.color.return_colored("Car removed from file", 'red')))
        time.sleep(1.5)
        self.cars()

    def register_car(self):
        self.frame.delete_last_lines(8)

        self.check_if_valid('Car type', self.vehicle_manager.check_type)

        self.check_if_valid('Make', self.vehicle_manager.check_make)

        self.check_if_valid('Model', self.vehicle_manager.check_model)

        self.check_if_valid('Year', self.vehicle_manager.check_year)
    
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
                ['Order','Customer','Cars', 'Report an error','Sign out'],
                'action'
            )
            self.handle_answer_from_menu(prompt['action'], 'main_menu')

    def handle_answer_from_menu(self, prompt, menu_type):

        ######################################################
        #                      MAIN MENU                     #                                                                                
        ######################################################
        if menu_type == 'main_menu':
            if prompt.lower() == 'sign out':
                self.signout() 
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
                print()
                self.frame.delete_last_lines(7)
                self.find_order()    
        ######################################################    
        #                      FIND ORDER                    #
        ######################################################
        elif menu_type == 'find order':
            if prompt.lower() == 'find order by id':
                self.frame.delete_last_lines(5)
                self.find_order_by_id()

            elif prompt.lower() == 'find order by ssn':
                self.frame.delete_last_lines(5)
                self.find_customer_by_ssn()

            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(5)
                self.order()

        ######################################################    
        #                      CUSTOMER                      #
        ######################################################

        elif menu_type == 'customer':
            if prompt.lower() == 'go back':
                self.frame.delete_last_lines(5)
                self.init_menu()

            elif prompt.lower() == 'register customer':
                print()
                self.register_customer()

            elif prompt.lower() == 'find customer':
                self.frame.delete_last_lines(5)
                self.find_customer()
        
        ######################################################    
        #                    REGISTER CUSTOMER               #                    
        ######################################################
        elif menu_type == 'register customer':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(13)
                self.save_new_customer()
                self.customer()

            elif prompt.lower() == 'cancel':
                self.frame.delete_last_lines(15)
                self.customer()
                
        ######################################################    
        #                  SAVE EDITED CUSTOMER              #                    
        ######################################################
        elif menu_type == 'save edited customer':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(15)
                self.save_edited_customer()
                print('Customer: {}\n'.format(self.__current_customer.__str__()))
                self.found_customer()

            elif prompt.lower() == 'cancel':
                self.frame.delete_last_lines(15)
                print('Customer: {}\n'.format(self.__current_customer.__str__()))
                self.found_customer()

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
            chosen,customers = prompt
            if chosen['customer'].lower() != 'go back':
                self.__current_customer = customers[chosen['index']]
                self.frame.delete_last_lines(8)
                print('Customer: ' + self.__current_customer.__str__())
                print()
                self.found_customer()
            else:
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
                    if detail == 'Credit card number':
                        print("{}: **** **** **** {}".format(detail, value[12:]))
                        continue
                    if detail == 'SSN':
                        print('{}: {}-{}'.format(detail, value[:6], value[6:]))
                        continue
                    print("{}: {}".format(detail, value))
                self.nocco_list.single_list('Go back')
                self.frame.delete_last_lines(10)
                print('Customer: ' + self.__current_customer.__str__() +'\n')
                self.found_customer()

            elif prompt.lower() == 'edit customer':
                self.frame.delete_last_lines(6)
                self.edit_customer()

            elif prompt.lower() == 'unsubscribe customer':
                self.frame.delete_last_lines(5)
                self.delete_customer()
                self.frame.delete_last_lines()

            elif prompt.lower() == 'go back':
                self.frame.delete_last_lines(6)
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
                self.frame.delete_last_lines(2)
                self.frame.delete_last_lines(7)
                self.find_cars()
                self.cars()

            elif prompt.lower() == 'show all available cars':
                self.frame.delete_last_lines(9)
                self.show_all_available_cars()
                print()
                print()
                self.cars()

            elif prompt.lower() == 'show cars in service':
                self.frame.delete_last_lines(9)
                self.show_cars_in_service()
                print()
                print()
                self.cars()
            elif prompt.lower() == 'show cars that require maintenance':
                self.frame.delete_last_lines(9)
                self.show_cars_that_require_maintenance()
                print()
                print()
                self.cars()

            elif prompt.lower() == 'show cars that must be checked':
                self.frame.delete_last_lines(9)
                self.show_cars_in_service()
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
            elif prompt.lower() == 'calculate order':
                self.frame.delete_last_lines(14)
                self.frame.delete_last_lines(5)
                self.calculate_order()



                
        ######################################################    
        #                    FIND CAR                        #                    
        ######################################################
        elif menu_type == 'find car':
            if prompt.lower() == 'find car by number plate':
                self.frame.delete_last_lines(7)
                self.find_cars_by_number_plate()

            elif prompt.lower() == 'find car by make':
                self.frame.delete_last_lines(7)
                self.find_cars_by_make()

            elif prompt.lower() == 'find car by type':
                self.frame.delete_last_lines(7)
                self.find_cars_by_type()

            elif prompt.lower() == 'go back':
                # It goes in cars menu if go back is chosen!
                self.cars()

        ######################################################    
        #                    FOUND CAR                       #                    
        ######################################################
        elif menu_type == 'found car':
            if prompt.lower() == 'edit car':
                self.frame.delete_last_lines(5)
                self.init_menu()
                # TODO edit car

            elif prompt.lower() == 'remove car':
                self.frame.delete_last_lines(5)
                self.delete_vehicle()

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

        ######################################################    
        #               SHOW CARS IN SERVICE                 #                    
        ######################################################
        elif menu_type == 'show cars in service':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(16)
                self.save_new_car()
                print("\n" * 7)
                self.cars()

            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(10)
                self.cars()

        ######################################################    
        #       CARS THAT REQUIRE MAINTENANCE               #                    
        ######################################################
        elif menu_type == 'show cars that require maintenance':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(16)
                self.save_new_car()
                print("\n" * 7)
                self.cars()

            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(10)
                self.cars()

        ######################################################    
        #            CARS THAT MUST BE CHECKED               #                    
        ######################################################
        elif menu_type == 'show cars that must be checked':
            if prompt.lower() == 'save':
                self.frame.delete_last_lines(16)
                self.save_new_car()
                print("\n" * 7)
                self.cars()

            if prompt.lower() == 'cancel':
                self.frame.delete_last_lines(10)
                self.cars()
