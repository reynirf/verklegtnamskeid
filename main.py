from models.vehicle import Vehicle
from ui.frame import Frame
from lib.color import Color
from models.employee import Employee
from lib.nocco_list import NoccoList



def get_employees():
    with open('data/ids.txt') as employees:
        raw_employees = employees.read()

    employees = {}
    for employee in raw_employees.split('\n'):
        employees[employee[0:3]] = employee[4:]
    return employees

def authenticate(employees):
    try:
        employee_id = input('Enter ID: ')
        employees[employee_id]
        return (employees[employee_id],employee_id)
    except KeyError:
        Frame.delete_last_lines(2)
        Color.print_colored('Invalid ID: ' + employee_id, 'red')
        return authenticate(employees)

def initialize_employee(employee):
    name = employee[0]
    employee_id = employee[1]
    employee = Employee(name,employee_id)
    return employee

def introduce_employee(employee):
    Frame.delete_last_lines(2)
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
