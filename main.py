from ui.frame import Frame
from ui.menu import Menu


#STARTING FUNCTIONALITY

frame = Frame()
frame.clear()
print(frame)
print() # empty line before system boot

frame.boot_system()

frame.delete_last_lines(3)

menu = Menu()

menu.authenticate_v2()

menu.init_menu()
