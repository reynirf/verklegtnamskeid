from ui.frame import Frame
from ui.menu import Menu

frame = Frame()  # init frame

frame.clear_window()  # clear console/terminal window

print(frame)  # prints frame (logo and horizontal line)

frame.boot_system()  # boot system. Progress bar from 0-100%

menu = Menu()  # init menu

menu.authenticate()  # authenticate  

menu.init_menu()  # after authentication, show main menu
