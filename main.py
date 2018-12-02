from models.vehicle import Vehicle
from ui.frame import Frame
from lib.color import Color
from models.employee import Employee
from lib.nocco_list import NoccoList
import csv
import time
import getpass

def get_employees():
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

def authenticate(employees, has_failed=0):
    try:
        employee_id = input('Enter ID: ')
        employee_password = getpass.getpass('Enter password: ')

        employees[employee_id] #test to see if the employee_id exists. If it doesn't exist, it will raise a KeyError
        
        if employee_password != employees[employee_id]['password']:
            raise ValueError
        return (employees[employee_id],employee_id),has_failed
    except KeyError:
        has_failed = True
        Frame.delete_last_lines(3)
        Color.print_colored('Invalid ID: ' + employee_id, 'red')
        return authenticate(employees,has_failed)
    except ValueError:
        has_failed = True
        Frame.delete_last_lines(3)
        Color.print_colored('Wrong password', 'red')
        return authenticate(employees,has_failed)

def initialize_employee(employee):
    info = employee[0]
    employee_id = employee[1]
    password = info['password']
    name = info['name']
    employee = Employee(name,employee_id,password)
    return employee

def introduce_employee(employee):
    Frame.delete_last_lines(3)
    print(employee)

def authenticate_process(employees):
    print() #ekki remove'a
    print()
    employee,has_failed = authenticate(employees)
    print()
    employee = initialize_employee(employee)
    if has_failed:
        Frame.delete_last_lines(4)
        print()
        print()
        print()
        print()
    introduce_employee(employee)
    print()

    return employee

def logout(employee, employees):
    Frame.delete_last_lines(8)
    print('{} has been logged out'.format(Color.return_colored(employee.get_name(), 'red')))
    time.sleep(2)
    Frame.delete_last_lines(3)
    return authenticate_process(employees)

def handle_answer_from_menu(prompt, employee, employees):
    if prompt.lower() == 'logout':
        new_employee = logout(employee, employees) #logout and return the next user who logs into the syste
        menu(new_employee, employees)
        return new_employee
        


def menu(employee, employees):
    prompt = NoccoList.choose_one('Choose an action', ['Order','Customer','Reports','Logout'],'action')
    employee = handle_answer_from_menu(prompt['action'], employee, employees)


frame = Frame()
print(frame) #ekki remove'a

employees = get_employees()
employee = authenticate_process(employees)
menu(employee, employees)




print() 
# print('The action you picked: ' + prompt['answer'])

print()
print()



# for i in Color.COLORS:
#     Color.print_colored('tetetssteta', i)
# # Color.print_colored('HALHAHLALOHLAHLA', 'blue')
