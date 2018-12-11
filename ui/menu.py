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
		self.__current_order = ""

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
											  [
												'Register customer', 
												'Find customer', 
												'Go back'
											  ],
											  'action')
		self.handle_answer_from_menu(customer['action'], 'customer')

	def order(self):
		order_list = self.nocco_list.choose_one("Choose an action",
												[
													"Register order",
													"Find order",
													"Show pricing list", 
													"Go back"
												],
												"action")
		self.handle_answer_from_menu(order_list['action'], 'order')

	def calculate_order(self):
		print()
		print()
		print('{:<20}{:>10}{:>12}'.format('Description', 'Per day', 'Amount'))
		print('-'*42)
		base_price, insurance, extra_ins, days = self.order_manager.calculate_order()
		print('{:<20}{:>10}{:>12}'.format('Base price', base_price, base_price*days))
		print('{:<20}{:>10}{:>12}'.format('Basic insurance', insurance, insurance*days))
		print('{:<20}{:>10}{:>12}'.format('Extra insurance', extra_ins, extra_ins*days))
		print('-'*42)
		total = (base_price + insurance + extra_ins) * days
		print('{:<20}{:>22}'.format('TOTAL ISK:', total))

		self.nocco_list.single_list("Go back")

	def show_pricing_list(self):
		self.frame.delete_last_lines(2)
		print()
		with open("./data/prices_list.txt","r") as f:
			for i in f:
				print("\t",i)
		self.nocco_list.single_list("Go back")
		self.frame.delete_last_lines(10)
		self.order()

	def find_order_by_id(self):
		ID = input("Enter ID: ")
		self.frame.delete_last_lines(2)
		print()
		order = self.order_manager.find_order_by_id(ID)
		if order == None:
			print('{}'.format(self.color.return_colored("Order not found!", 'red')))
			time.sleep(1.5)
			self.frame.delete_last_lines()
			self.find_order()
		else:
			self.__current_order = order
			print("Order: " + order.__str__())
			print()
			self.__current_order = order
			self.found_order()

	def find_order_by_ssn(self):
		ssn = input("Enter SSN: ")
		print()
		orders = self.order_manager.find_order_by_ssn(ssn)
		if orders == []:
			print('{}'.format(self.color.return_colored("Order not found", 'red')))
			time.sleep(1.5)
			self.frame.delete_last_lines(3)
			self.find_order()
		else:
			self.frame.delete_last_lines(2)
			if len(orders) == 1:
				print("Order : " + orders[0].__str__())
				print()
				self.__current_order = orders[0]
				self.found_order()
			else:
				print("{}".format(self.color.return_colored("There are multiple orders with that SSN!", 'red')))
				print()
				printable_orders = ['ID: {} | SSN: {} | {} - {}'.format(
					order.__str__(),order.get_ssn(), order.get_dates()[0], order.get_dates()[1]) for order in orders]
				printable_orders.append('Go back')

				found_multiple_orders = self.nocco_list.choose_one('Choose an order',
						printable_orders, 'order', True)
				self.handle_answer_from_menu((found_multiple_orders, orders), 
						'found multiple orders')

	def find_order(self):
		find_order_list = self.nocco_list.choose_one('Choose an action',
						['Find order by ID', 'Find order by SSN', 'Go back'], 'action')
		self.handle_answer_from_menu(find_order_list['action'], 'find order')

	def found_order(self):
		found_order_list = self.nocco_list.choose_one('Choose an action',
						['Edit order', 'Print order', 'Delete order', 'Go back'], 'action')
		self.frame.delete_last_lines(2)
		self.handle_answer_from_menu(found_order_list['action'], 'found order')

	def get_inputted_order(self):
		cars = self.order_manager.get_inputted_order()
		self.frame.delete_last_lines(len(cars) - 1)
		register_order_list = self.nocco_list.choose_one("Choose an action",["Save", "Calculate order" , "Cancel"], "action")
		self.handle_answer_from_menu(register_order_list['action'], 'register_order')

	def delete_order(self):
		start_day, end_day = self.__current_order.get_dates()
		dates = self.order_manager.get_order_dates(start_day, end_day)
		car = self.__current_order.get_license_plate()
		self.vehicle_manager.delete_order_dates(dates, car)
		self.order_manager.delete_order(self.__current_order)
		self.frame.delete_last_lines(2)
		print('{}'.format(self.color.return_colored("Order removed", 'red')))
		time.sleep(1.5)
		self.frame.delete_last_lines(1)
		self.order()

	def save_new_order(self):
		self.order_manager.save_new_order()
		print("{}".format(self.color.return_colored("New order registered", 'green')))
		time.sleep(2)
		dates = self.order_manager.get_order_dates()
		vehicle = self.order_manager.get_license_plate()
		self.vehicle_manager.save_order_dates(dates, vehicle)

	def register_order(self):
		self.frame.delete_last_lines(6)
		print()

		self.check_if_valid('order ID', self.order_manager.check_ID)

		self.check_if_valid('customer SSN', self.order_manager.check_ssn)

		self.check_if_valid('start date (DD MM YYYY)', self.order_manager.check_start_date)

		self.check_if_valid('ending date (DD MM YYYY)', self.order_manager.check_ending_date)

		self.check_if_valid('pick up time', self.order_manager.check_pick_up_time)

		self.check_if_valid('returning time', self.order_manager.check_returning_time)

		self.check_if_valid('pick up location (Reykjavik or Akureyri)', self.order_manager.check_pick_up_location)

		self.check_if_valid('return location (Reykjavik or Akureyri)', self.order_manager.check_return_location)
		
		self.check_if_valid('type of vehicle (Small car, sedan, offroad or bus)', self.order_manager.check_type_of_vehicle)
		
		start_date, end_date = self.order_manager.get_dates()
		car_list = self.vehicle_manager.show_car_availability(start_date, end_date, 'available')
		car_type = self.order_manager.get_type()
		filtered_list = self.vehicle_manager.find_car_by_type(car_type, car_list)
		print()
		if not filtered_list:
			self.frame.delete_last_lines(1)
			print()
			print("No vehicle of type {} available on these dates".format(self.color.return_colored(car_type, 'red')))
			time.sleep(2)
			self.frame.delete_last_lines(11)
			self.order()
		else:
			print('Available cars:')
			print()
			print('{:<20} {:<20} {:<20} {:<20}'.format('License', 'Make', 'Model', 'Seats'))
			print('-'*70)
			for car in filtered_list:
				print(car.availability_string())
			print()

			self.check_if_valid('license plate', self.order_manager.check_license_plate)

			self.check_if_valid('insurance (yes or no)', self.order_manager.check_insurance)

			print()
			register_order_list = self.nocco_list.choose_one("Choose an action", ["Save", "Calculate order", "Cancel"], "action")
			self.frame.delete_last_lines(len(filtered_list) + 5)
			
			self.handle_answer_from_menu(register_order_list['action'], 'register_order')
	
	def edit_order(self):
		order = self.__current_order.return_details()
		print('{}\n'.format(self.color.return_colored('Leave input empty to keep the value the same', 'green')))

		self.check_if_valid('ID', self.order_manager.check_ID, True, order['ID'])

		self.check_if_valid('SSN', self.order_manager.check_ssn, True, order['SSN'])

		self.check_if_valid('start date', self.order_manager.check_start_date, True, order['Start date'])

		self.check_if_valid('start date', self.order_manager.check_ending_date, True, order['End date'])

		self.check_if_valid('pick up time', self.order_manager.check_pick_up_time, True, order['Pick up time'])

		self.check_if_valid('return time', self.order_manager.check_returning_time, True, order['Return time'])

		self.check_if_valid('pick up location', self.order_manager.check_pick_up_location, True,
							order['Pick up location'])

		self.check_if_valid('Return location', self.order_manager.check_return_location, True, 
							order['Return location'])
		
		self.check_if_valid('type', self.order_manager.check_type_of_vehicle, True, order['Type'])

		# start_date, end_date = self.order_manager.get_dates()
		# car_list = self.vehicle_manager.show_car_availability(start_date, end_date, 'available')
		# car_type = self.order_manager.get_type()
		# filtered_list = self.vehicle_manager.find_car_by_type(car_type, car_list)
		# print()
		# if not filtered_list:
		# 	self.frame.delete_last_lines(1)
		# 	print()
		# 	print("No vehicle of type {} available on these dates".format(self.color.return_colored(car_type, 'red')))
		# 	time.sleep(2)
		# 	self.frame.delete_last_lines(13)
		# 	self.order()
		# else:
		# 	print('Available cars:')
		# 	print()
		# 	print('{:<20} {:<20} {:<20} {:<20}'.format('Licence', 'Make', 'Model', 'Seats'))
		# 	print('-'*70)
		# 	for car in filtered_list:
		# 		print(car.availability_string())
		# 	print()

		self.check_if_valid('license plate', self.order_manager.check_license_plate, True, order['License plate'])

		self.check_if_valid('insurance', self.order_manager.check_insurance, True, order['Insurance'])

		print()
		save_edited_order = self.nocco_list.choose_one('Choose an action',
														  ['Save', 'Cancel'],
														  'action')
		self.handle_answer_from_menu(save_edited_order['action'], 'save edited order')
	
	def save_edited_order(self):
		self.order_manager.delete_order(self.__current_order)
		self.order_manager.save_new_order()
		print("{}".format(self.color.return_colored("Order updated", 'green')))
		time.sleep(1.5)

	def check_if_valid(self, to_enter, to_check, editing=False, current_value=''):
		mistake = 0
		error = "check if valid"
		while error:
			if not editing and not current_value:
				user_input = input("Enter " + to_enter + ": ")
			else:
				if to_enter == 'Credit card number':
					user_input = input("Enter " + to_enter + " [**** **** **** " + current_value[12:] + "]: ")
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
					if to_enter == 'Credit card number':
						print("Enter " + to_enter + " [**** **** **** " + current_value[12:] + "]: " + "**** **** **** " + current_value[12:])
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
													   ['Save', 'Cancel'],
													   'action')
		self.handle_answer_from_menu(register_customer['action'], 'register customer')

	def edit_customer(self):
		customer = self.__current_customer.return_details()
		print('{}\n'.format(self.color.return_colored('Leave input empty to keep the value the same', 'green')))

		self.check_if_valid('Name', self.customer_manager.check_name, True, customer['Name'])

		self.check_if_valid('SSN', self.customer_manager.check_ssn, True, customer['SSN'])

		self.check_if_valid('Birthday', self.customer_manager.check_birthday, True, customer['Birthday'])

		self.check_if_valid('Phone number', self.customer_manager.check_phone_number, True, customer['Phone number'])

		self.check_if_valid('Driver license category', self.customer_manager.check_license, True,
							customer['Driver license category'])

		self.check_if_valid('Email address', self.customer_manager.check_email, True, customer['Email address'])

		self.check_if_valid('Credit card number', self.customer_manager.check_credit_card, True,
							customer['Credit card number'])

		self.check_if_valid('Home address', self.customer_manager.check_address, True, customer['Home address'])

		print()
		save_edited_customer = self.nocco_list.choose_one('Choose an action',
														  ['Save', 'Cancel'],
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
												   ['Find customer by Name', 'Find customer by SSN', 'Go back'],
												   'action')
		self.handle_answer_from_menu(find_customer['action'], 'find customer')

	def found_customer(self):
		found_customer = self.nocco_list.choose_one('Choose an action',
													['Print customer details', 'Edit customer', 'Unsubscribe customer',
													 'Go back'], 'action')
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
				print("Customer: " + self.__current_customer.__str__())
				print()
				self.found_customer()
			else:
				print("{}".format(self.color.return_colored("There are multiple customers with that name!", 'red')))
				print()
				printable_customers = [
					'{} | {}-{}'.format(customer.__str__(), customer.get_ssn()[:6], customer.get_ssn()[6:]) for customer
					in customers]

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
		print('{}'.format(self.color.return_colored("Customer removed", 'red')))
		time.sleep(1.5)
		self.frame.delete_last_lines()
		self.customer()

	def save_new_car(self):
		self.vehicle_manager.save_new_car()
		print("{}".format(self.color.return_colored("New car registered!", 'green')))
		time.sleep(1.5)
		self.frame.delete_last_lines(2)

	def show_car_availability(self, prompt):
		self.check_if_valid('a start date [DD/MM/YYYY]', self.order_manager.check_start_date)
		self.check_if_valid('an end date [DD/MM/YYYY]', self.order_manager.check_ending_date)
		start_date, end_date = self.order_manager.get_dates()
		car_list = self.vehicle_manager.show_car_availability(start_date, end_date, prompt)
		print() 
		print('{:<20} {:<20} {:<20} {:<20}'.format('License', 'Make', 'Model', 'Seats'))
		print('-'*70)
		for car in car_list:
			print(car.availability_string())

		self.nocco_list.single_list('Go back')
		self.frame.delete_last_lines(len(car_list) + 1)

	def show_cars_that_require_maintenance(self):
		test_data = [['Toyota', 'Huyndai', 'Ford', 'Reynir', 'Sixarinn'],
					 ['Renault', 'Viddi', 'Peugot', 'Guðrún', 'Ermir'], ['Nike', 'Subaru', 'Volvo', 'Bíll', 'Hilux']]

		col_width = max(len(word) for row in test_data for word in row) + 2
		for row in test_data:
			print("".join(word.ljust(col_width) for word in row))

		self.nocco_list.single_list('Go back')

	def show_cars_that_must_be_checked(self):
		test_data = [['Toyota', 'Huyndai', 'Ford', 'Reynir', 'Sixarinn'],
					 ['Renault', 'Viddi', 'Peugot', 'Guðrún', 'Ermir'], ['Nike', 'Subaru', 'Volvo', 'Bíll', 'Hilux']]

		col_width = max(len(word) for row in test_data for word in row) + 2
		for row in test_data:
			print("".join(word.ljust(col_width) for word in row))

		self.nocco_list.single_list('Go back')

	def cars(self):
		self.frame.delete_last_lines(7)
		car = self.nocco_list.choose_one('Choose an action', ['Register car', 'Find car', 'Show all available cars',
															  'Show cars in service',
															  'Go back'], 'action')
		self.handle_answer_from_menu(car['action'], 'cars')

	def find_cars(self):
		find_cars = self.nocco_list.choose_one('Choose an action', ['Find car by number plate', 'Find car by make',
																	'Find car by type', 'Go back'], 'action')
		print()
		self.handle_answer_from_menu(find_cars['action'], 'find car')

	def find_cars_by_license_plate(self):
		license_plate = input("Enter license plate: ")
		print()
		car = self.vehicle_manager.find_car_by_license_plate(license_plate)
		if car == None:
			print('{}'.format(self.color.return_colored("Car not found!", 'red')))
			self.frame.delete_last_lines(3)
			time.sleep(1.5)
			self.find_cars()
		else:
			print("Car: " + car.get_license())
			print()
			self.__current_vehicle = car
			found_cars_list = self.nocco_list.choose_one(
														"Choose an action", 
														[
															"Edit car", 
															"Remove car", 
															"Go back"
														], 
														"action"
														)
			self.frame.delete_last_lines(2)
			self.handle_answer_from_menu(found_cars_list['action'], 'found car')

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
			for i, car in enumerate(cars):
				print("Car " + str(i + 1) + ": " + car.get_make())
				time.sleep(1.5)
			print()

	def find_cars_by_type(self):
		type_of_car = input("Enter type: ")
		print()
		cars = self.vehicle_manager.find_car_by_type(type_of_car)
		if cars == None:
			print('{}'.format(self.color.return_colored("No cars found!", 'red')))
			time.sleep(1.5)
			self.frame.delete_last_lines(3)
			self.find_cars()
		else:
			for i, car in enumerate(cars):
				print("Car " + str(i + 1) + ": " + car.get_license())
				# time.sleep(1.5)
			print()
			if len(cars) == 1:
				self.__current_vehicle = cars
				found_cars_list = self.nocco_list.choose_one(
																"Choose an action", 
																[
																	"Edit car", 
																	"Remove car", 
																	"Go back"
																], 
																"action"
															)
				self.frame.delete_last_lines(2)
				self.handle_answer_from_menu(found_cars_list['action'], 'found car')

	def delete_vehicle(self):
		self.vehicle_manager.delete_vehicle(self.__current_vehicle)
		self.frame.delete_last_lines(1)
		print('{}'.format(self.color.return_colored("Car removed", 'red')))
		time.sleep(1.5)
		self.cars()

	def register_car(self):
		self.frame.delete_last_lines(7)

		self.check_if_valid('Car type (smallcar, sedan, offroad or bus)', self.vehicle_manager.check_type)

		self.check_if_valid('Make', self.vehicle_manager.check_make)

		self.check_if_valid('Model', self.vehicle_manager.check_model)

		self.check_if_valid('Year', self.vehicle_manager.check_year)

		self.check_if_valid('Number of seats', self.vehicle_manager.check_number_of_seats)

		self.check_if_valid('License plate', self.vehicle_manager.check_license_plate)

		self.check_if_valid('Fuel (bensin, diesel, electric or hybrid)', self.vehicle_manager.check_fuel)

		self.check_if_valid('Driving transmission (manual or automatic)', self.vehicle_manager.check_driving_transmission)
		print()
		register_car = self.nocco_list.choose_one('Choose an action',
												  ['Save', 'Cancel'],
												  'action')
		self.handle_answer_from_menu(register_car['action'], 'register car')

	def init_menu(self):
		prompt = self.nocco_list.choose_one(
			'Choose an action',
			['Order', 'Customer', 'Cars', 'Report an error', 'Sign out'],
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
				self.frame.delete_last_lines(2)
				self.register_order()

			elif prompt.lower() == 'find order':
				print()
				self.frame.delete_last_lines(7)
				self.find_order()
			elif prompt.lower() == 'show pricing list':
				print()
				self.frame.delete_last_lines(6)
				self.show_pricing_list()
		######################################################    
		#                      FIND ORDER                    #
		######################################################
		elif menu_type == 'find order':
			if prompt.lower() == 'find order by id':
				self.frame.delete_last_lines(5)
				self.find_order_by_id()

			elif prompt.lower() == 'find order by ssn':
				self.frame.delete_last_lines(5)
				self.find_order_by_ssn()

			elif prompt.lower() == 'go back':
				self.frame.delete_last_lines(5)
				self.order()

		######################################################    
		#                     FOUND ORDER                    #
		######################################################
		elif menu_type == 'found order':
			if prompt.lower() == 'edit order':
				self.frame.delete_last_lines(6)
				self.edit_order()
			elif prompt.lower() == 'print order':
				order_details = self.__current_order.return_details()
				self.frame.delete_last_lines(6)
				for detail, value in order_details.items():
					print("{}: {}".format(detail, value))
				self.nocco_list.single_list('Go back')
				self.frame.delete_last_lines(13)
				print('Order: ' + self.__current_order.__str__() + '\n')
				self.found_order()
			elif prompt.lower() == 'delete order':
				self.frame.delete_last_lines(4)
				self.delete_order()
			elif prompt.lower() == 'go back':
				self.frame.delete_last_lines(6)
				self.find_order()
		
		######################################################    
		#                    save edited order                   #
		######################################################
		elif menu_type == 'save edited order':
			if prompt.lower() == 'save':
				self.frame.delete_last_lines(18)
				self.save_edited_order()
				self.frame.delete_last_lines()
				print('Order: {}\n'.format(self.__current_order.__str__()))
				self.found_order()
			if prompt.lower() == 'cancel':
				self.frame.delete_last_lines(18)
				print('Order: {}\n'.format(self.__current_order.__str__()))
				self.found_order()

		######################################################    
		#                 FOUND MULTIPLE ORDERS              #                    
		######################################################
		if menu_type == 'found multiple orders':
			chosen, orders = prompt
			self.frame.delete_last_lines(5 + len(orders))
			if chosen['order'].lower() != 'go back':
				self.__current_order = orders[chosen['index']]
				print('Order: ' + self.__current_order.__str__())
				print()
				self.found_order()
			else:
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
			chosen, customers = prompt
			self.frame.delete_last_lines(len(customers) + 5)
			if chosen['customer'].lower() != 'go back':
				self.__current_customer = customers[chosen['index']]
				print('Customer: ' + self.__current_customer.__str__())
				print()
				self.found_customer()
			else:
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
				print('Customer: ' + self.__current_customer.__str__() + '\n')
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
				self.register_car()
				self.cars()

			if prompt.lower() == 'find car':
				self.frame.delete_last_lines(7)
				self.find_cars()
				self.cars()

			elif prompt.lower() == 'show all available cars':
				self.frame.delete_last_lines(7)
				self.show_car_availability('available')
				self.frame.delete_last_lines(1)
				print()
				print()
				self.cars()

			elif prompt.lower() == 'show cars in service':
				self.frame.delete_last_lines(7)
				self.show_car_availability('rented')
				self.frame.delete_last_lines(1)
				print()
				print()
				self.cars()

			elif prompt.lower() == 'go back':
				self.frame.delete_last_lines(7)
				self.init_menu()
		########################################################
		#                SHOW PRICING LIST                     #
		########################################################
		elif menu_type == 'show pricing list':
			if prompt.lower() == 'go back':
				self.frame.delete_last_lines(9)
				self.order()

		########################################################
		#                REGISTER NEW ORDER                    #
		########################################################
		elif menu_type == 'register_order':
			if prompt.lower() == 'cancel':
				self.frame.delete_last_lines(18)
				self.order()

			elif prompt.lower() == 'save':
				self.frame.delete_last_lines(18)
				self.save_new_order()
				self.frame.delete_last_lines()
				self.order()

			elif prompt.lower() == 'calculate order':
				self.frame.delete_last_lines(19)
				self.calculate_order()
				self.frame.delete_last_lines(10)
				self.get_inputted_order()
	
		######################################################    
		#                    FIND CAR                        #                    
		######################################################
		elif menu_type == 'find car':
			if prompt.lower() == 'find car by number plate':
				self.frame.delete_last_lines(7)
				self.find_cars_by_license_plate()

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
				self.frame.delete_last_lines(13)
				self.save_new_car()
				print("\n" * 7)
				self.cars()

			if prompt.lower() == 'cancel':
				self.frame.delete_last_lines(6)
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
		#       CARS THAT REQUIRE MAINTENANCE                #                    
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
