from models.vehicle import Vehicle
from ui.frame import Frame
from lib.color import Color
from models.employee import Employee
from lib.nocco_list import NoccoList
import csv



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

def authenticate(employees):
    try:
        employee_id = input('Enter ID: ')
        employee_password = input('Enter password: ')
        employees[employee_id]
        if employee_password != employees[employee_id]['password']:
            raise ValueError
        return (employees[employee_id],employee_id)
    except KeyError:
        Frame.delete_last_lines(3)
        Color.print_colored('Invalid ID: ' + employee_id, 'red')
        return authenticate(employees)
    except ValueError:
        Frame.delete_last_lines(3)
        Color.print_colored('Wrong password', 'red')
        return authenticate(employees)

def initialize_employee(employee):
    print(employee)
    info = employee[0]
    employee_id = employee[1]
    password = info['password']
    name = info['name']
    employee = Employee(name,employee_id,password)
    return employee

def introduce_employee(employee):
    Frame.delete_last_lines(5)
    print(employee)

# def logout(employee):
#     Frame.delete_last_lines(12)

frame = Frame()
print(frame) #ekki remove'a

employees = get_employees()
print() #ekki remove'a
employee = authenticate(employees)

print() 

employee = initialize_employee(employee)
introduce_employee(employee)

print()

prompt = NoccoList.choose_one('Choose an action', ['Order','Customer','Reports','Logout'],'answer')

print() 
print('The action you picked: ' + prompt['answer'])

print()
print()



# for i in Color.COLORS:
#     Color.print_colored('tetetssteta', i)
# # Color.print_colored('HALHAHLALOHLAHLA', 'blue')
