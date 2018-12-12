from ui.frame import Frame
from ui.menu import Menu

frame = Frame()
frame.clear_window()
print(frame) # prints frame (logo and horizontal line)

print() # empty line before system boot

frame.boot_system() # boot system. Progress bar from 0-100%

frame.delete_last_lines(3) # delete 3 lines to remove the progress bar after it's finished

menu = Menu() # init menu

menu.authenticate() # authenticate  

menu.init_menu() # after authentication, show main menu
