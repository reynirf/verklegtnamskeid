from lib.nocco_list import NoccoList
from lib.color import Color
from ui.frame import Frame
from models.employee import Employee
from models.customer import Customer
from models.price import Price
from service.employee_manager import EmployeeManager
from service.customer_manager import CustomerManager
from service.vehicle_manager import VehicleManager
from service.order_manager import OrderManager
import csv
import time
import getpass
import os.path


class Menu:
	"""Handle all the menu functionalities.
	self.frame.delete_last_lines(xx) will be found in many places of our code, 
	because it deletes the previous lines for better look, as we decided in the design pattern.
	"""
	def __init__(self):
		self.nocco_list = NoccoList()
		self.color = Color()
		self.frame = Frame()
		self.employee_manager = EmployeeManager()
		self.customer_manager = CustomerManager()
		self.vehicle_manager = VehicleManager()
		self.order_manager = OrderManager()
		self.price_list = Price()
		self.__current_customer = ""
		self.__current_vehicle = ""
		self.__current_order = ""

	def authenticate(self):
		"""This method check the authentication of the employee, by entering the username and password,
		and it will loop until it has the correct username and password.
		"""
		print()
		print()
		logged_in = False
		while logged_in == False:
			employee_id = input("Enter your ID: ")
			employee_password = getpass.getpass("Enter password: ")
			response = self.employee_manager.authenticate(employee_id, employee_password)
			if type(response) == Employee:  # The function authenticate checks the id and password.
				print()  # Styling...
				if self.employee_manager.has_failed():
					self.frame.delete_last_lines(4)
					print("\n" * 3)
				self.introduce_employee(response)  # The function introduce_employee prints the customer
				print()
				logged_in = True  # To end the while loop
			else:
				self.frame.delete_last_lines(3)
				self.color.print_colored(response, "red")  # The loggin has failed.

	def introduce_employee(self, employee):
		"""Prints the name of the employee.
		"""
		self.frame.delete_last_lines(3)
		print(employee)

	def signout(self):
		"""In case that the employee signs out, it prints sign out and calls the authenticate() method to wait
		for the employee to sign in again.
		"""
		self.frame.delete_last_lines(9)
		employee = self.employee_manager.get_current_employee() 
		print("{} has been logged out".format(  				# Prints that the user has been logged out
			self.color.return_colored(employee.get_name(), "red")))
		time.sleep(1.5)  # Lets the program sleep for 1.5 seconds before continuing for a regular flow.
		self.frame.delete_last_lines(3)
		self.authenticate()

	def check_if_valid(self, to_enter, to_check, editing=False, current_value=""):
		"""Controls the output for most of our error checks."""
		mistake = 0
		error = "check if valid"
		while error:
			if (not editing and not current_value) or (not current_value and type(editing) == list):
				user_input = input("Enter " + to_enter + ": ")
			else:
				if to_enter == "Credit card number":
					user_input = input("Enter " + to_enter + " [**** **** **** " + current_value[12:] + "]: ")
				else:
					user_input = input("Enter " + to_enter + " [" + current_value + "]: ")
			error = to_check(user_input, editing, current_value)
			if editing and current_value and not error:
				if mistake:
					self.frame.delete_last_lines(2)
				else:
					self.frame.delete_last_lines()
				if user_input != "":
					print("Enter " + to_enter + " [" + current_value + "]: " + user_input)
				else:
					if to_enter == "Credit card number":  # Hides first 12 numbers and prints only last 4 numbers.
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

	def invalid_input(self, message):
		"""If an invalid input is entered then this method is called and,
		provides the correct error message to suggest why it the inputed data is wrong and how it 
		can be fixed.
		"""
		self.frame.delete_last_lines(1)
		print("{}".format(self.color.return_colored(message, "red")))
				
	############################################################################
	#       Here starts the main menu and all the methods that go with it      #
	############################################################################
	
	def handle_answer_from_main_menus(self, prompt, menu_type):
		"""This method handles all the choices that are made when choosing from the 
		main menus of the application.
		"""
		####################################################
		#                    MAIN MENU                     #                                                                                
		####################################################
		if menu_type == "main_menu":

			if prompt == "Sign out":
				self.signout()
				self.init_menu()

			elif prompt == "Report an error":
				self.report_error()
				self.init_menu()

			elif prompt == "Customer":
				self.frame.delete_last_lines(7)
				self.customer()

			elif prompt == "Vehicle":
				self.vehicles()

			elif prompt == "Order":
				self.frame.delete_last_lines(7)
				self.order()

		####################################################    
		#                    ORDER                         #
		####################################################

		elif menu_type == "order":

			if prompt == "Go back":
				self.frame.delete_last_lines(6)
				self.init_menu()

			elif prompt == "Register order":
				print()
				self.frame.delete_last_lines(2)
				self.register_order()

			elif prompt == "Find order":
				print()
				self.frame.delete_last_lines(7)
				self.find_order()

			elif prompt == "Show pricing list":
				print()
				self.frame.delete_last_lines(6)
				self.show_pricing_list()
				self.frame.delete_last_lines(6)
				self.order()

		####################################################    
		#                    CUSTOMER                      #
		####################################################

		elif menu_type == "customer":

			if prompt == "Go back":
				self.frame.delete_last_lines(5)
				self.init_menu()

			elif prompt == "Register customer":
				print()
				self.register_customer()

			elif prompt == "Find customer":
				self.frame.delete_last_lines(5)
				self.find_customer()

		####################################################    
		#                     VEHICLES                     #                    
		####################################################
		elif menu_type == "vehicles":
			
			if prompt == "Register vehicle":
				self.register_vehicle()
				self.vehicles()

			if prompt == "Find vehicle":
				self.frame.delete_last_lines(7)
				self.find_vehicles()
				self.vehicles()

			elif prompt == "Show all available vehicles":
				self.frame.delete_last_lines(7)
				self.show_vehicle_availability("available")
				print()
				print()
				self.vehicles()

			elif prompt == "Show vehicles in service":
				self.frame.delete_last_lines(7)
				self.show_vehicle_availability("rented")
				print()
				print()
				self.vehicles()

			elif prompt == "Go back":
				self.frame.delete_last_lines(7)
				self.init_menu()
	
	def init_menu(self):
		"""Initial menu/Homepage,
		The employee can choose any of the operations and continue with the functionalities of the page, or he/she can sign out,
		and from there the it will be called the authenticate() method which prompts to get an user id and password."""
		prompt = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Order", 
				"Customer", 
				"Vehicle", 
				"Report an error", 
				"Sign out"
			],
			"action"
		)
		self.handle_answer_from_main_menus(prompt["action"], "main_menu")

	def report_error(self):
		"""Since we do not have any database for holding email and password online as a form to prove the employee
		identity, or troubleshooting, we simply implemented a simple method for any problems encountered while
		using this service, the employee should contact the manager of this service for technical support.
		This method prints how to reach help, and then go back at the main page.
		"""
		self.frame.delete_last_lines(7)
		print("Contact your manager to report an error.")
		self.nocco_list.single_list("Go back")
		self.frame.delete_last_lines(3)

	def customer(self):
		"""Prints functionalities of the customer menu, and the user can either choose any option from
		the menu, either can go back at main menu.
		"""
		customer = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Register customer", 
				"Find customer", 
				"Go back"
			],
			"action"
		)
		self.handle_answer_from_main_menus(customer["action"], "customer")

	def order(self):
		"""Prints functionalities of the order menu, and the user can either choose any option from
		the menu, either can go back at main menu.
		"""
		order_list = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Register order",
				"Find order",
				"Show pricing list", 
				"Go back"
			],
			"action"
		)
		self.handle_answer_from_main_menus(order_list["action"], "order")

	def vehicles(self):
		"""This function allows the user to choose what action he wants after going to the section "cars"
		using nocco list"""
		self.frame.delete_last_lines(7)
		vehicle = self.nocco_list.choose_one(
			"Choose an action", 
			[
				"Register vehicle", 
				"Find vehicle", 
				"Show all available vehicles",
				"Show vehicles in service",
				"Go back"
			], 
			"action"
		)
		self.handle_answer_from_main_menus(vehicle["action"], "vehicles")
	
	############################################################################
	#      Here starts the order menu and all the methods that go with it      #
	############################################################################

	def handle_answer_from_order_menus(self, prompt, menu_type):
		"""This method handles all the choices that are made when choosing from the 
		order submenus of the application.
		"""
		######################################################
		#                REGISTER NEW ORDER                  #
		######################################################
		if menu_type == 'register_order':
			if prompt == 'Cancel':
				self.order()

			elif prompt == 'Save':
				self.save_new_order()
				self.frame.delete_last_lines(2)
				orders = self.order_manager.get_order_list()
				self.__current_order = orders[-1]
				print()
				print("Order: {}\n".format(self.__current_order.__str__()))
				self.found_order()

			elif prompt == 'Calculate order':			
				self.calculate_order()
				self.frame.delete_last_lines(10)				
				print()
				self.get_inputted_order()
	
		####################################################    
		#                    FIND ORDER                    #
		####################################################
		elif menu_type == "find order":

			if prompt == "Find order by ID":
				self.frame.delete_last_lines(5)
				self.find_order_by_id()

			elif prompt == "Find order by SSN":
				self.frame.delete_last_lines(5)
				self.find_order_by_ssn()

			elif prompt == "Go back":
				self.frame.delete_last_lines(5)
				self.order()

		####################################################    
		#                   FOUND ORDER                    #
		####################################################
		elif menu_type == "found order":

			if prompt == "Edit order":
				self.frame.delete_last_lines(6)
				self.edit_order()

			elif prompt == "Print order":
				order_details = self.__current_order.return_details()
				self.frame.delete_last_lines(6)
				for detail, value in order_details.items():
					print("{}: {}".format(detail, value))
				self.nocco_list.single_list("Go back")
				self.frame.delete_last_lines(13)
				print("Order: " + self.__current_order.__str__() + "\n")
				self.found_order()

			elif prompt == "Delete order":
				self.frame.delete_last_lines(4)
				self.delete_order()

			elif prompt == "Go back":
				self.frame.delete_last_lines(6)
				self.find_order()
		
		####################################################    
		#                 SAVE EDITED ORDER                #
		####################################################
		elif menu_type == "save edited order":

			if prompt == "Save":
				self.frame.delete_last_lines(18)
				self.save_edited_order()
				self.frame.delete_last_lines()
				try:
					temp_order = self.order_manager.find_order_by_id(self.__current_order.get_id())
					if not temp_order:
						raise ValueError
					self.__current_order = temp_order
				except ValueError:
					temp_order = self.order_manager.find_order_by_ssn(self.__current_order.get_ssn())
					if temp_order:
						self.__current_order = temp_order[-1]
				print("Order: {}\n".format(self.__current_order.__str__()))
				self.found_order()

			if prompt == "Cancel":
				self.frame.delete_last_lines(18)
				print("Order: {}\n".format(self.__current_order.__str__()))
				self.found_order()

		####################################################    
		#               FOUND MULTIPLE ORDERS              #                    
		####################################################
		if menu_type == "found multiple orders":
			chosen, orders = prompt
			self.frame.delete_last_lines(5 + len(orders))
			if chosen["order"] != "Go back":
				self.__current_order = orders[chosen["index"]]
				print("Order: " + self.__current_order.__str__())
				print()
				self.found_order()
			else:
				self.order()   

	def calculate_order(self):
		"""After the employee has inputed all the neccessary data, it calculates the order in a readable style,
		with correct formating.
		"""
		print('{:<20}{:>10}{:>12}'.format('Description', 'Per day', 'Amount'))
		print('-'*42)
		base_price, insurance, extra_ins, days = self.order_manager.calculate_order()
		print("{:<20}{:>10}{:>12}".format("Base price", base_price, base_price*days))
		print("{:<20}{:>10}{:>12}".format("Basic insurance", insurance, insurance*days))
		print("{:<20}{:>10}{:>12}".format("Extra insurance", extra_ins, extra_ins*days))
		print("-"*42)
		total = (base_price + insurance + extra_ins) * days
		print("{:<20}{:>22}".format("TOTAL ISK:", total))
		# A lot of formatting was needed to print the calculated order fancy and readable.
		self.nocco_list.single_list("Go back")

	def show_pricing_list(self):
		"""This simple method prints the pricing list, in case that the customer wants to know whaat kind of car 
		can afford, and what the price ranges is.
		"""
		vehicle_types = ["smallcar", "sedan", "offroad", "bus"]  # All available types we offer.
		self.frame.delete_last_lines(2)
		print()
		print("{:<15}{:>12}{:>20}{:>20}".format("Vehicle type", "Base price", "Basic insurance", "Extra insurance"))
		print("-"*67)
		for vehicle in vehicle_types:  # Loops the vehicle list and prints the price for each vehicle.
			print(self.price_list.print_prices(vehicle))
		print()
		print("Prices are per day in ISK")
		self.nocco_list.single_list("Go back")
		self.frame.delete_last_lines(10)
		self.order()  # Runs order again after you go back.
	
	def find_order(self):
		"""This method provides the functionalities of the Find order in Order menu. 
		The employee can either user enter either right arrow to continue in any desired option. 
		"""
		find_order_list = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Find order by ID",
				"Find order by SSN", 
				"Go back"
			], 
			"action"
		)
		self.handle_answer_from_order_menus(find_order_list["action"], "find order")

	def find_order_by_id(self):
		"""This method makes possible for the employee to find any order in the database (csv) with the id of the order.
		And after the order is found, it provides further options to continue.
		"""
		ID = input("Enter ID: ")
		self.frame.delete_last_lines(2)
		print()
		order = self.order_manager.find_order_by_id(ID)  # Runs find_order_by_id in order manager
		if order == None:  # Then there is no order with that particular ID
			print("{}".format(self.color.return_colored("Order not found!", "red")))
			time.sleep(1.5)
			self.frame.delete_last_lines()
			self.find_order()
		else:  # The order has been found
			self.__current_order = order
			print("Order: " + order.__str__())
			print()
			self.found_order() 

	def find_order_by_ssn(self):
		"""This method makes possible for the employee to find any order in the database (csv) with the SSN of the customer.
		And after the order is found, it provides further options to continue.
		"""
		ssn = input("Enter SSN: ")
		print()
		orders = self.order_manager.find_order_by_ssn(ssn)  # Runs find_order_by_ssn in order_manager
		if orders == []:  # Than the order has not been found because there is no order linked to that ssn
			print("{}".format(self.color.return_colored("Order not found!", "red")))
			time.sleep(1.5)
			self.frame.delete_last_lines(3)
			self.find_order()
		else:  # A order has been found with that particular ssn linked to it.
			self.frame.delete_last_lines(2)
			if len(orders) == 1:  # There is only one order linked to that particular ssn
				print("Order : " + orders[0].__str__())
				print()
				self.__current_order = orders[0]
				self.found_order()
			else:  # Multiple orders are linked with a paticullar ssn
				print("{}".format(self.color.return_colored("There are multiple orders with that SSN!", "red")))
				print()
				printable_orders = ["ID: {} | {} - {}".format(
					order.__str__(), order.get_dates()[0], order.get_dates()[1]) for order in orders]
				printable_orders.append("Go back")
				# Reynir...

				found_multiple_orders = self.nocco_list.choose_one(
					"Choose an order",
					printable_orders, 
					"order", 
					True
				)
				self.handle_answer_from_order_menus((found_multiple_orders, orders), "found multiple orders")

	def found_order(self):
		"""After the employee has found the order that was looking for, this method provides the functionalities
		of what the employee can do with that particular order.
		"""
		found_order_list = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Edit order", 
				"Print order", 
				"Delete order", 
				"Go back"
			], 
			"action"
		)
		self.frame.delete_last_lines(2)
		self.handle_answer_from_order_menus(found_order_list["action"], "found order")

	def get_inputted_order(self):
		"""After the employee has entered all the neccessary datas about the order, then another menu will
		appear with the functionalities to move on in further operations.
		"""
		self.order_manager.get_inputted_order()
		print()
		register_order_list = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Save", 
				"Calculate order" , 
				"Cancel"
			], 
			"action"
		)
		self.frame.delete_last_lines(19)
		self.handle_answer_from_order_menus(register_order_list['action'], 'register_order')

	def delete_order(self):
		""" This method enables the employee to delete/cancel any order. """
		start_day, end_day = self.__current_order.get_dates()  # gets start day an end day from get_dates.
		dates = self.order_manager.get_order_dates(start_day, end_day)  # puts the values in get_order_dates
		vehicle = self.__current_order.get_license_plate()  # Gets a license plate for current order.
		self.vehicle_manager.delete_order_dates(dates, vehicle)  # A function that deletes the dates a vehicle is rented.
		self.order_manager.delete_order(self.__current_order)  # A function that deletes the particullar order
		self.frame.delete_last_lines(2)
		print("{}".format(self.color.return_colored("Order deleted!", "red")))
		time.sleep(1.5)
		self.frame.delete_last_lines(1)
		self.order()

	def save_new_order(self):
		"""Saves a new order in our csv database if the correct information is entered."""
		self.order_manager.save_new_order()  # A function that saves the order in the csv file.
		print("{}".format(self.color.return_colored("New order registered!", "green")))  # Prits this message in case that a new order is successfully registered
		time.sleep(1.5)
		dates = self.order_manager.get_order_dates()  # Allows to input only available date, and provides from inputing e.g past date
		vehicle = self.order_manager.get_license_plate()
		self.vehicle_manager.save_order_dates(dates, vehicle)  # saves the dates for a praticullar rented car.

	def register_order(self):
		"""When the employee wants to register a new order, this method is called and enables the employee to enter the correct information, 
		by calling the correct checks for each data entered.
		Some of the datas that are available, are just a choice for simplicity by the decision of the developers, like 
		ability to choose only from two places, Reykjavik or Akureyri. 
		After the employee has entered all the neccessary datas that are required, then another sub menu is provided to allow the customer to 
		pick a car in a range of available cars. After the customer has choose the car, then the employee can proceed in further options.
		"""
		self.frame.delete_last_lines(6)
		print()
		# Here are all checks to check if a input is valid, it is sent to the check_if_valid function
		# and order_manager checks.

		self.check_if_valid("order ID", self.order_manager.check_ID)

		self.check_if_valid("customer SSN", self.order_manager.check_ssn)

		self.check_if_valid("start date (DD.MM.YYYY)", self.order_manager.check_start_date)

		self.check_if_valid("ending date (DD.MM.YYYY)", self.order_manager.check_ending_date)

		self.check_if_valid("pick up time (HRS:MIN)", self.order_manager.check_pick_up_time)

		self.check_if_valid("returning time (HRS:MIN)", self.order_manager.check_returning_time)

		self.check_if_valid("pick up location (Reykjavik or Akureyri)", self.order_manager.check_pick_up_location)

		self.check_if_valid("return location (Reykjavik or Akureyri)", self.order_manager.check_return_location)
		
		self.check_if_valid("type of vehicle (Small car, sedan, offroad or bus)", self.order_manager.check_type_of_vehicle)
		
		start_date, end_date = self.order_manager.get_dates()
		vehicle_list = self.vehicle_manager.show_vehicle_availability(start_date, end_date, "available")
		# Shows only the cars that are available in that time
		vehicle_type = self.order_manager.get_type()
		filtered_list = self.vehicle_manager.find_vehicle_by_type(vehicle_type, vehicle_list)
		print()
		if not filtered_list:  # In case that there are not any available car. 
			self.frame.delete_last_lines(1)
			print()
			print("No vehicle of type {} available on these dates.".format(self.color.return_colored(vehicle_type, "red")))
			time.sleep(1.5)
			self.frame.delete_last_lines(11)
			self.order()
		else:  # Otherwise it will display all the cars available and the customer can pick any.
			plates = []
			print("Available vehicles:")
			print()
			print("{:<20} {:<20} {:<20} {:<20}".format("License", "Make", "Model", "Seats"))
			print("-"*70)
			for vehicle in filtered_list:
				print(vehicle.availability_string())
				plates.append(vehicle.get_license().lower())
			print()

			self.check_if_valid("license plate", self.order_manager.check_license_plate, plates)

			self.check_if_valid("insurance (yes or no)", self.order_manager.check_insurance) 
			# Let the customer choose if he/she wants any insurance other than basic.

			print()
			register_order_list = self.nocco_list.choose_one(
				"Choose an action", 
				[
					"Save", 
					"Calculate order", 
					"Cancel"
				], 
				"action"
			)
			self.frame.delete_last_lines(len(filtered_list) + 23)
			self.handle_answer_from_order_menus(register_order_list["action"], "register_order")
	
	def edit_order(self):
		"""This method is called when the customer or employee wants to edit any order.
		The employee has the ability to change or leave as it is any data.
		Any data that wants to be changed can be done by entering the new data and then hit enter, otherwise if the employee wants
		to keep the previous data can skip editing by leaving the input field empty and hit enter.
		For each data, it is called check method to check if the data entered is correct, or in correct format.
		"""
		order = self.__current_order.return_details()
		print("{}\n".format(self.color.return_colored("Leave input empty to keep the value the same.", "green")))
		# Checks if inputs are valid, goes thorugh check_if_valid fundtion and checks in order_manager.
		
		self.check_if_valid("ID", self.order_manager.check_ID, True, order["ID"])

		self.check_if_valid("SSN", self.order_manager.check_ssn, True, order["SSN"])

		self.check_if_valid("start date", self.order_manager.check_start_date, True, order["Start date"])

		self.check_if_valid("end date", self.order_manager.check_ending_date, True, order["End date"])

		self.check_if_valid("pick up time", self.order_manager.check_pick_up_time, True, order["Pick up time"])

		self.check_if_valid("return time", self.order_manager.check_returning_time, True, order["Return time"])

		self.check_if_valid("pick up location", self.order_manager.check_pick_up_location, True, order["Pick up location"])

		self.check_if_valid("Return location", self.order_manager.check_return_location, True, order["Return location"])
		
		self.check_if_valid("type", self.order_manager.check_type_of_vehicle, True, order["Type"])

		self.check_if_valid("license plate", self.order_manager.check_license_plate, True, order["License plate"])

		self.check_if_valid("insurance", self.order_manager.check_insurance, True, order["Insurance"])

		print()
		save_edited_order = self.nocco_list.choose_one("Choose an action", ["Save", "Cancel"], "action")
		self.handle_answer_from_order_menus(save_edited_order["action"], "save edited order")
	
	def save_edited_order(self):
		"""Updates the order after it is edited by the employee.
		First deletes the previous order, and then saves the edited order as a new order.
		"""
		self.order_manager.delete_order(self.__current_order)
		self.order_manager.save_new_order()
		print("{}".format(self.color.return_colored("Order updated!", "green")))
		time.sleep(1.5)

	############################################################################
	#    Here starts the customer menu and all the methods that go with it     #
	############################################################################

	def handle_answer_from_customer_menus(self, prompt, menu_type):
		"""This method handles all the choices that are made when choosing from the 
		customer submenus of the application.
		"""
		####################################################    
		#                  REGISTER CUSTOMER               #                    
		####################################################
		if menu_type == "register customer":

			if prompt == "Save":
				self.frame.delete_last_lines(12)
				self.save_new_customer()
				customers = self.customer_manager.get_customer_list()
				self.__current_customer = customers[-1]
				print("Customer: {}\n".format(self.__current_customer.__str__()))
				self.found_customer()

			elif prompt == "Cancel":
				self.frame.delete_last_lines(12)
				self.customer()

		####################################################    
		#                SAVE EDITED CUSTOMER              #                    
		####################################################
		elif menu_type == "save edited customer":

			if prompt == "Save":
				self.frame.delete_last_lines(14)
				self.save_edited_customer()
				self.__current_customer = self.customer_manager.find_customer_by_ssn(self.__current_customer.get_ssn())
				print("Customer: {}\n".format(self.__current_customer.__str__()))
				self.found_customer()

			elif prompt == "Cancel":
				self.frame.delete_last_lines(14)
				print("Customer: {}\n".format(self.__current_customer.__str__()))
				self.found_customer()

		####################################################    
		#                  FIND CUSTOMER                   #                    
		####################################################
		elif menu_type == "find customer":

			if prompt == "Find customer by name":
				self.frame.delete_last_lines(5)
				self.find_customer_by_name()

			elif prompt == "Find customer by SSN":
				self.frame.delete_last_lines(5)
				self.find_customer_by_ssn()

			elif prompt == "Go back":
				self.frame.delete_last_lines(5)
				self.customer()

		####################################################    
		#                  FOUND CUSTOMER                  #                    
		####################################################
		if menu_type == "found customer":

			if prompt == "Print customer details":
				customer_details = self.__current_customer.return_details()
				self.frame.delete_last_lines(6)
				for detail, value in customer_details.items():
					if detail == "Credit card number":
						print("{}: **** **** **** {}".format(detail, value[12:]))
						continue
					if detail == "SSN":
						print("{}: {}-{}".format(detail, value[:6], value[6:]))
						continue
					print("{}: {}".format(detail, value))
				self.nocco_list.single_list("Go back")
				self.frame.delete_last_lines(9)
				print("Customer: " + self.__current_customer.__str__() + "\n")
				self.found_customer()

			elif prompt == "Print order history":
				self.frame.delete_last_lines(4)
				self.customer_history()
				self.found_customer()

			elif prompt == "Edit customer":
				self.frame.delete_last_lines(6)
				self.edit_customer()

			elif prompt == "Delete customer":
				self.frame.delete_last_lines(5)
				self.delete_customer()
				self.frame.delete_last_lines()

			elif prompt == "Go back":
				self.frame.delete_last_lines(6)
				self.find_customer()

		####################################################    
		#             FOUND MULTIPLE CUSTOMERS             #                    
		####################################################
		if menu_type == "found multiple customers":
			chosen, customers = prompt
			self.frame.delete_last_lines(len(customers) + 5)
			if chosen["customer"] != "Go back":
				self.__current_customer = customers[chosen["index"]]
				print("Customer: " + self.__current_customer.__str__())
				print()
				self.found_customer()
			else:
				self.customer()

	def register_customer(self):
		"""Method for registering a new customer.
		Provides all the required checks to prevent the employee entering wrong inputs.
		After the employee has entered all required datas, then another sub menu will appear, 
		to select an action for either save the customer or can cancel and go back.
		"""
		self.frame.delete_last_lines(6)

		self.check_if_valid("Name", self.customer_manager.check_name)

		self.check_if_valid("SSN", self.customer_manager.check_ssn)

		self.check_if_valid("Phone number", self.customer_manager.check_phone_number)

		self.check_if_valid("Driver license category", self.customer_manager.check_license)

		self.check_if_valid("Email address", self.customer_manager.check_email)

		self.check_if_valid("Credit card number", self.customer_manager.check_credit_card)

		self.check_if_valid("Home address", self.customer_manager.check_address)

		print()
		register_customer = self.nocco_list.choose_one("Choose an action", ["Save", "Cancel"], "action")
		self.handle_answer_from_customer_menus(register_customer["action"], "register customer")

	def edit_customer(self):
		"""In case that the employee wants to edit a customer´s data then first the employee must find that particular customer and then this method
		is called, the logic behind is similar as in edit_order(),
		The employee can either add new data, and it will override the previous date or can leave the input field
		empty and hit enter, then the previous data will be kept unchanged.
		"""
		customer = self.__current_customer.return_details()
		print("{}\n".format(self.color.return_colored("Leave input empty to keep the value the same.", "green")))

		self.check_if_valid("Name", self.customer_manager.check_name, True, customer["Name"])

		self.check_if_valid("SSN", self.customer_manager.check_ssn, True, customer["SSN"])

		self.check_if_valid("Phone number", self.customer_manager.check_phone_number, True, customer["Phone number"])

		self.check_if_valid("Driver license category", self.customer_manager.check_license, True,
							customer["Driver license category"])

		self.check_if_valid("Email address", self.customer_manager.check_email, True, customer["Email address"])

		self.check_if_valid("Credit card number", self.customer_manager.check_credit_card, True,
							customer["Credit card number"])

		self.check_if_valid("Home address", self.customer_manager.check_address, True, customer["Home address"])

		print()
		save_edited_customer = self.nocco_list.choose_one("Choose an action", ["Save", "Cancel"], "action")
		self.handle_answer_from_customer_menus(save_edited_customer["action"], "save edited customer")

	def save_new_customer(self):
		"""When a new customer is saved a short message to let the employee 
		that the operation was done successfully is printed in green
		for a short period of time and the it disappears.
		"""
		self.customer_manager.save_new_customer()
		print("{}".format(self.color.return_colored("New customer registered!", "green")))
		time.sleep(1.5)
		self.frame.delete_last_lines(1)

	def save_edited_customer(self):
		"""When saving an edited customer, first it deletes the previous incorrect customer
		and then saves the edited customer as new.
		"""
		self.customer_manager.delete_customer(self.__current_customer)
		self.customer_manager.save_new_customer()
		
		print("{}".format(self.color.return_colored("Customer updated!", "green")))
		time.sleep(1.5)
		self.frame.delete_last_lines(1)

	def find_customer(self):
		"""When find customer option is clicked, the employee will choose to find a customer either by name, either by SSN.
		Find customer by SSN in our opinion is more efficient because of the nature of the SSN that is unique for each customer.
		"""
		find_customer = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Find customer by name", 
				"Find customer by SSN", 
				"Go back"
			],
			"action"
		)
		self.handle_answer_from_customer_menus(find_customer["action"], "find customer")

	def found_customer(self):
		"""After the unique customer is found, then the employee can decide what to do with that particular customer,
		by clicking in any of the available options.
		"""
		found_customer = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Print customer details", 
				"Print order history", 
				"Edit customer", 
				"Delete customer",
				"Go back"
			], 
			"action"
		)
		self.frame.delete_last_lines(3)
		self.handle_answer_from_customer_menus(found_customer["action"], "found customer")

	def customer_history(self):
		"""If the employee wants to see the history of any particular customer, after the employee has found the customer,
		this method is called and it will print all the available orders made by that customer, or print a message
		in case that the customer has never made any order.
		"""
		ssn = self.__current_customer.get_ssn()
		orders = self.order_manager.find_order_by_ssn(ssn)
		if orders == []:
			print("{}".format(self.color.return_colored("No orders registered to this customer", "red")))
			self.nocco_list.single_list("Go back")
			self.frame.delete_last_lines(3)	
		else:
			print("{:<10}{:<10}{:<20}".format("ID", "Vehicle", "Dates"))
			print("-"*43)
			for order in orders:
				print("{:<10}{:<10}{:>20}".format(order.get_id(), order.get_license_plate(), order.get_date_str()))
			self.nocco_list.single_list("Go back")
			self.frame.delete_last_lines(len(orders) + 4)

	def find_customer_by_name(self):
		"""If the employee is looking for a customer by the name of that customer, this method is called
		The employee enters the customer´s name, and in case that it does not exist any customer with that particuar name,
		a short message will be printed to indiciate that. 
		In case that there are more than one customer with a particular name then a message will be printed to indicate that, 
		and the list of the cusomers will be printed in the screen for the employee to choose from.
		In case that there is only one customer with that name, then the employee will be able to edit, or delete that customer.
		"""
		name = input("Enter name: ")
		print()
		customers = self.customer_manager.find_customer_by_name(name)
		if customers == None: #Then there is no customer, none will go through here...
			print("{}".format(self.color.return_colored("Customer not found!", "red")))
			time.sleep(1.5)
			self.frame.delete_last_lines(4)
			print()
			self.find_customer()
		else: #If the customer is found
			self.frame.delete_last_lines(2)
			if len(customers) == 1: #If there is only one customer
				self.__current_customer = customers[0] #The first index
				print("Customer: " + self.__current_customer.__str__())
				print()
				self.found_customer()
			else: #Else there must be at least more than one customer that are found.
				print("{}".format(self.color.return_colored("There are multiple customers with that name!", "red")))
				print()
				printable_customers = [
					"{}".format(customer.__str__()) for customer #loops through the list of customers found.
					in customers]

				printable_customers.append("Go back")
				found_multiple_customers = self.nocco_list.choose_one("Choose customer", printable_customers, "customer", True)

				self.handle_answer_from_customer_menus((found_multiple_customers, customers), "found multiple customers")

	def find_customer_by_ssn(self):
		"""This method is called when the employee wants to find a customer, because it uses SSN as criteria for search
		and because SSN is unique for each customer, this method of finding customers is much more efficient than finding customers by name,
		because many customers can have the same name, but only one customer can have one SSN, so this method enables the employee to have more power
		and being more effiecient in search, and editing or deleting the customer afterwards.
		"""
		#Very similar to finding customer by name...
		ssn = input("Enter SSN: ")
		print()
		customer = self.customer_manager.find_customer_by_ssn(ssn)
		if customer == None:
			print("{}".format(self.color.return_colored("Customer not found!", "red")))
			time.sleep(1.5)
			self.frame.delete_last_lines(4)
			print()
			self.find_customer()
		else: #... except for here because there can only be one customer with a particullar ssn.
			self.frame.delete_last_lines(2)
			self.__current_customer = customer
			print("Customer: " + customer.__str__())
			print()
			self.found_customer()

	def delete_customer(self):
		"""When the employee wants to delete a customer, this method is called,
		first the employee has to find the customer then can delete.
		A short message will show to indicate that the customer is successfully deleted.
		"""
		self.customer_manager.delete_customer(self.__current_customer) #this functuonality deletes the
																		#customer from the csv file.
		self.frame.delete_last_lines()
		print("{}".format(self.color.return_colored("Customer deleted!", "red")))
		time.sleep(1.5)
		self.frame.delete_last_lines()
		self.customer()

	############################################################################
	#    Here starts the vehicle menu and all the methods that go with it      #
	############################################################################

	def handle_answer_from_vehicle_menus(self, prompt, menu_type):
		"""This method handles all the choices that are made when choosing from the 
		vehicle submenus of the application.
		"""
		####################################################    
		#                  REGISTER VEHICLE                #                    
		####################################################
		if menu_type == "register vehicle":

			if prompt == "Save":
				self.frame.delete_last_lines(13)
				self.save_new_vehicle()
				vehicles = self.vehicle_manager.get_vehicle_list()
				self.__current_vehicle = vehicles[-1]
				print()
				print("Vehicle: {}\n".format(self.__current_vehicle.__str__()))
				self.found_vehicle()

			if prompt == "Cancel":
				self.frame.delete_last_lines(6)
				self.vehicles()		

		####################################################    
		#                   FIND VEHICLE                   #                    
		####################################################
		elif menu_type == "find vehicle":

			if prompt == "Find vehicle by license plate":
				self.frame.delete_last_lines(7)
				self.find_vehicles_by_license_plate()

			elif prompt == "Find vehicle by make":
				self.frame.delete_last_lines(7)
				self.find_vehicles_by_make()

			elif prompt == "Find vehicle by type":
				self.frame.delete_last_lines(7)
				self.find_vehicles_by_type()

			elif prompt == "Go back":
				# It goes in vehicles menu if go back is chosen!
				self.vehicles()

		####################################################    
		#                   FOUND VEHICLE                  #                    
		####################################################
		elif menu_type == "found vehicle":

			if prompt == "Edit vehicle":
				self.frame.delete_last_lines(8)
				self.edit_vehicle()

			elif prompt == "Delete vehicle":
				self.frame.delete_last_lines(8)
				self.delete_vehicle()

			elif prompt == "Print vehicle":

				vehicle_details = self.__current_vehicle.return_details()
				self.frame.delete_last_lines(9)
				for detail, value in vehicle_details.items():
					print("{}: {}".format(detail, value))
				self.nocco_list.single_list("Go back")
				self.frame.delete_last_lines(10)
				print("Vehicle: " + self.__current_vehicle.__str__() + "\n")
				self.found_vehicle()
			
			elif prompt == "Print vehicle history":
				self.frame.delete_last_lines(7)
				self.vehicle_history()
				self.found_vehicle()

			elif prompt == "Go back":
				self.frame.delete_last_lines(9)
				self.find_vehicles()
				
		####################################################    
		#             FOUND MULTIPLE VEHICLES              #                    
		####################################################
		elif menu_type == "found multiple vehicles":
			chosen, vehicles = prompt
			if chosen["vehicle"] != "Go back":
				self.frame.delete_last_lines(len(vehicles) + 5)
				self.__current_vehicle = vehicles[chosen["index"]]
				print("Vehicle: " + self.__current_vehicle.__str__())
				print()
				self.found_vehicle()
			else:
				self.frame.delete_last_lines(len(vehicles) + 4)
				print("\n" * 5)
				self.vehicles()

		####################################################    
		#                SAVE EDITED VEHICLE               #                    
		####################################################
		elif menu_type == "save edited vehicle":

			if prompt == "Save":
				self.frame.delete_last_lines(15)
				self.save_edited_vehicle()
				self.frame.delete_last_lines()
				self.__current_vehicle = self.vehicle_manager.find_vehicle_by_license_plate(self.vehicle_manager.get_license())
				print("Vehicle: {}\n".format(self.__current_vehicle.__str__()))
				self.found_vehicle()
				self.frame.delete_last_lines(2)

			if prompt == "Cancel":
				self.frame.delete_last_lines(15)
				print("Vehicle: {}\n".format(self.__current_vehicle.__str__()))
				self.found_vehicle()
				self.frame.delete_last_lines(2)

		####################################################    
		#             SHOW VEHICLES IN SERVICE             #                    
		####################################################
		elif menu_type == "show vehicles in service":

			if prompt == "Save":
				self.frame.delete_last_lines(16)
				self.save_new_vehicle()
				print("\n" * 7)
				self.vehicles()

			if prompt == "Cancel":
				self.frame.delete_last_lines(10)
				self.vehicles()

	def save_new_vehicle(self):
		"""this function saves a new registered vehicle in the vehicles csv file, it calls another function;
		save_new_vehicle, inside of vehicle_manager that makes up the functionality for saving a vehivle.
		"""
		self.vehicle_manager.save_new_vehicle()
		print("{}".format(self.color.return_colored("New vehicle registered!", "green")))
		time.sleep(1.5)
		self.frame.delete_last_lines(2)

	def register_vehicle(self):
		"""Here we check if a inut from the employee is valid or not. If it is not valid the empoyee is
		informed and asked to inpt the right input. It goes through check_if_valid function and check functions
		in vehicle_manager.
		"""
		self.frame.delete_last_lines(7)

		self.check_if_valid("Vehicle type (smallcar, sedan, offroad or bus)", self.vehicle_manager.check_type)

		self.check_if_valid("Make", self.vehicle_manager.check_make)

		self.check_if_valid("Model", self.vehicle_manager.check_model)

		self.check_if_valid("Year", self.vehicle_manager.check_year)

		self.check_if_valid("Number of seats", self.vehicle_manager.check_number_of_seats)

		self.check_if_valid("License plate", self.vehicle_manager.check_license_plate)

		self.check_if_valid("Fuel (gasoline, diesel, electric or hybrid)", self.vehicle_manager.check_fuel)

		self.check_if_valid("Driving transmission (manual or automatic)", self.vehicle_manager.check_driving_transmission)
		print()
		register_vehicle = self.nocco_list.choose_one("Choose an action", ["Save", "Cancel"], "action")
		self.handle_answer_from_vehicle_menus(register_vehicle["action"], "register vehicle")

	def find_vehicles(self):
		"""Here the employee is shown available actions after he chooses the action "find vehicle". This
		is doable with the help of nocco_list
		"""
		find_vehicles = self.nocco_list.choose_one("Choose an action", ["Find vehicle by license plate", "Find vehicle by make",
																	"Find vehicle by type", "Go back"], "action")
		print()
		self.handle_answer_from_vehicle_menus(find_vehicles["action"], "find vehicle")

	def find_vehicles_by_license_plate(self):
		"""This function handles if the user wants to find vehicles by license plate, the input is compared
		to the data stored in vehicle_manager.
		"""
		license_plate = input("Enter license plate: ")
		print()
		vehicle = self.vehicle_manager.find_vehicle_by_license_plate(license_plate)
		if vehicle == None: #If there is no licence plate compared to the input, None will be the case.
			print("{}".format(self.color.return_colored("Vehicle not found!", "red")))
			self.frame.delete_last_lines(3)
			time.sleep(1.5)
			self.find_vehicles()
		else: # No need to check if there are many licence plates because there is only one licence plate
			# linked to a particullar car.
			self.frame.delete_last_lines(2)
			print("Vehicle: " + vehicle.get_license())
			print()
			self.__current_vehicle = vehicle
			found_vehicles_list = self.nocco_list.choose_one(
				"Choose an action", 
				[
					"Edit vehicle", 
					"Print vehicle",
					"Print vehicle history",
					"Delete vehicle", 
					"Go back"
				], 
				"action"
			)
			self.handle_answer_from_vehicle_menus(found_vehicles_list["action"], "found vehicle")

	def find_vehicles_by_make(self):
		"""This function handles if the user wants to find a vehicle by make."""
		make = input("Enter make: ")
		print()
		vehicles = self.vehicle_manager.find_vehicle_by_make(make)
		if vehicles == None: #similar to licence plate...
			print("{}".format(self.color.return_colored("No vehicle found!", "red")))
			time.sleep(1.5)
			self.frame.delete_last_lines(4)
			print()
			self.find_vehicles()
		else:
			self.frame.delete_last_lines(2)
			if len(vehicles) == 1: #Here we do need to check if there is only one make or many...
				self.__current_vehicle = vehicles[0]
				print("Vehicle: " + self.__current_vehicle.__str__())
				print()
				self.found_vehicle()
			else: #If there are many makes this will run.
				print("{}".format(self.color.return_colored("There are multiple vehicles with that make!", "red")))
				print()
				printable_vehicles = [
					"{}".format(vehicle.__str__()) for vehicle #Loops thorugh the list of all makes
					in vehicles]							   #compared to the make is being searched for.
					

				printable_vehicles.append("Go back")
				found_multiple_vehicles = self.nocco_list.choose_one("Choose vehicle", printable_vehicles, "vehicle", True)

				self.handle_answer_from_vehicle_menus((found_multiple_vehicles, vehicles), "found multiple vehicles")

	def find_vehicles_by_type(self):
		"""This function finds vehicles by type.
		"""
		type_of_vehicle = input("Enter type: ")
		print()
		vehicles = self.vehicle_manager.find_vehicle_by_type(type_of_vehicle)
		if vehicles == None: #Again very similar to finding makes or licence plates
			print("{}".format(self.color.return_colored("No vehicle found!", "red")))
			time.sleep(1.5)
			self.frame.delete_last_lines(4)
			print()
			self.find_vehicles()
		else:
			self.frame.delete_last_lines(2)
			if len(vehicles) == 1: #We do need to check if there are many types
				self.__current_vehicle = vehicles[0]
				print("Vehicle: " + self.__current_vehicle.__str__())
				print()
				self.found_vehicle()
			else: #If there are many types
				print("{}".format(self.color.return_colored("There are multiple vehicles with that type!", "red")))
				print()
				printable_vehicles = [
					"{} | {}".format(vehicle.__str__(), vehicle.get_vehicle_type()) for vehicle
					in vehicles]

				printable_vehicles.append("Go back")
				found_multiple_vehicles = self.nocco_list.choose_one("Choose vehicle", printable_vehicles, "vehicle", True)

				self.handle_answer_from_vehicle_menus((found_multiple_vehicles, vehicles), "found multiple vehicles")

	def found_vehicle(self):
		"""If the program has found a vehicle this function will take care of it, using nocco list the employee
		has options shown here down below.
		"""
		found_vehicle_list = self.nocco_list.choose_one(
			"Choose an action",
			[
				"Edit vehicle", 
				"Print vehicle", 
				"Print vehicle history", 
				"Delete vehicle", 
				"Go back"
			], 
			"action"
		)
		self.handle_answer_from_vehicle_menus(found_vehicle_list["action"], "found vehicle")											 

	def vehicle_history(self):
		"""This functon shows the history of a vehicle; what vehicle has been with what car.
		"""
		license_plate = self.__current_vehicle.get_license()
		order_list = self.order_manager.find_orders_by_vehicle(license_plate)
		if order_list == []: #the vehicle has no orders linked to it.
			print("{}".format(self.color.return_colored("No orders registered to this vehicle", "red")))
			self.nocco_list.single_list("Go back")
			self.frame.delete_last_lines(3)
		else: #The vehicle has a order linked to it.
			print("{:<10}{:<15}{:<20}".format("ID", "Customer SSN", "Dates"))
			print("-"*48)
			for order in order_list: #Loops throug the order_list
				print("{:<10}{:<15}{:>20}".format(order.get_id(), order.get_ssn(), order.get_date_str()))
				#Prints the id, ssn and dates for a order, using get functions in order.
			self.nocco_list.single_list("Go back")
			self.frame.delete_last_lines(len(order_list) + 4) #Styling, lines will vary on length of order_list.

	def edit_vehicle(self):
		"""This function is for editing a vehicle, we need to error check the input in editing like we did
		with registering, we can also use it to make editing easy.
		"""
		vehicle = self.__current_vehicle.return_details()
		self.frame.delete_last_lines()
		print("{}\n".format(self.color.return_colored("Leave input empty to keep the value the same", "green")))

		self.check_if_valid("Vehicle type", self.vehicle_manager.check_type, True, vehicle["Vehicle type"])

		self.check_if_valid("Make", self.vehicle_manager.check_make, True, vehicle["Make"])

		self.check_if_valid("Model", self.vehicle_manager.check_model, True, vehicle["Model"])

		self.check_if_valid("Year", self.vehicle_manager.check_year, True, vehicle["Year"])

		self.check_if_valid("Number of seats", self.vehicle_manager.check_number_of_seats, True, vehicle["Number of seats"])

		self.check_if_valid("License plate", self.vehicle_manager.check_license_plate, True, vehicle["License"])

		self.check_if_valid("Fuel", self.vehicle_manager.check_fuel, True, vehicle["Fuel"])

		self.check_if_valid("Driving transmission", self.vehicle_manager.check_driving_transmission, True, vehicle["Driving transmission"])
		print()

		save_edited_vehicle = self.nocco_list.choose_one("Choose an action", ["Save", "Cancel"], "action")
		self.handle_answer_from_vehicle_menus(save_edited_vehicle["action"], "save edited vehicle")
		self.frame.delete_last_lines(8)
		print("{}".format(self.color.return_colored("Vehicle Saved", "green")))
		time.sleep(4)
		
	def save_edited_vehicle(self):
		"""This function saves a edited vehicle, we first must delete it and then save it.
		"""
		self.vehicle_manager.delete_vehicle(self.__current_vehicle)
		self.vehicle_manager.save_new_vehicle()
		print("{}".format(self.color.return_colored("Vehicle updated!", "green")))
		time.sleep(1.5)

	def delete_vehicle(self):
		"""If the employee wants to delete a vehicle then after he/she has found the vehicle,
		then clicks in delete vehicle, and then this method is called.
		A short message to indicate that the operation was done successfully will be printed.
		"""
		self.vehicle_manager.delete_vehicle(self.__current_vehicle)
		self.frame.delete_last_lines(1)
		print("{}".format(self.color.return_colored("Vehicle deleted!", "red")))
		time.sleep(1.5)
		self.frame.delete_last_lines(2)
		print("\n" * 7)
		self.vehicles()
	
	def show_vehicle_availability(self, prompt):
		"""This method show all the vehicles that are available in a particular time, it will get only the vehicles that
		are not in renting and not ordered to be rent. Thats why the employee has to enter a start date and an
		end date to get the correct result.
		"""
		self.check_if_valid("a start date (DD.MM.YYYY)", self.order_manager.check_start_date)
		self.check_if_valid("an end date (DD.MM.YYYY)", self.order_manager.check_ending_date)
		start_date, end_date = self.order_manager.get_dates()
		vehicle_list = self.vehicle_manager.show_vehicle_availability(start_date, end_date, prompt)
		print() 
		print("{:<20} {:<20} {:<20} {:<20}".format("License", "Make", "Model", "Seats"))
		print("-"*70)
		for vehicle in vehicle_list:
			print(vehicle.availability_string())

		self.nocco_list.single_list("Go back")
		self.frame.delete_last_lines(len(vehicle_list) + 2)
