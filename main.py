from ui.frame import Frame
from ui.menu import Menu


#STARTING FUNCTIONALITY

frame = Frame()
#starting UI
frame.clear()
print(frame)

menu = Menu()

#employees = menu.get_employees()
employee = menu.authenticate_v2()
menu.init_menu(employee)




print() 
print()
print()
