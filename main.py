from ui.frame import Frame
from ui.menu import Menu


#STARTING FUNCTIONALITY

frame = Frame()
frame.clear()
print(frame)

menu = Menu()

menu.authenticate_v2()
menu.init_menu()