from datetime import datetime
from lib.color import Color
import sys
import os
import time

class Frame:
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    def __init__(self): 
        self.color = Color()
        self.get_size_of_screen()
        self.list_of_boot_length = list(range(0,3)) #when debugging
        # self.list_of_boot_length = list(range(0,50))

        self.logo = """
    .______    __   __          ___       __       _______  __    _______      ___      
    |   _  \  |  | |  |        /   \     |  |     |   ____||  |  /  _____|    /   \     
    |  |_)  | |  | |  |       /  ^  \    |  |     |  |__   |  | |  |  __     /  ^  \    
    |   _  <  |  | |  |      /  /_\  \   |  |     |   __|  |  | |  | |_ |   /  /_\  \   
    |  |_)  | |  | |  `----./  _____  \  |  `----.|  |____ |  | |  |__| |  /  _____  \  
    |______/  |__| |_______/__/     \__\ |_______||_______||__|  \______| /__/     \__\ 
                                                                                    
"""
    def get_size_of_screen(self):
        if os.name == 'nt':
            import shutil
            self.columns, self.rows = shutil.get_terminal_size()
        else:
            self.rows, self.columns = os.popen('stty size', 'r').read().split()

    def init_clock(self):
        while True:
            print(datetime.today().strftime("%H:%M:%S"), end="\r")
            time.sleep(1)

    def delete_last_lines(self, n=1):
        for _ in range(n):
            sys.stdout.write(Frame.CURSOR_UP_ONE)
            sys.stdout.write(Frame.ERASE_LINE)
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def boot_loop(self, iteration, total, prefix, suffix, length, decimals = 1, fill = '█'):
        """
            Loopa fyrir "boot system progress"
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = self.color.return_colored(fill,'green') * filled_length + '-' * (length - filled_length)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

        if iteration == total: 
            print() #prenta nýja línu þegar progressið er búið

    def boot_system(self):
        boot_length = len(self.list_of_boot_length)
        self.boot_loop(0, boot_length, 'Starting system:','Complete', 50)
        for number in self.list_of_boot_length:

            #delay for 0,1 seconds
            time.sleep(0.05) 

            #Uppfæra progress
            self.boot_loop(number + 1, boot_length, 'Starting system:', 'Complete', 50)

    def __str__(self):
        return '{}{}\n'.format(
            self.color.return_colored(self.logo,'bold'),
            self.color.return_colored('-'*int(self.columns), 'bold')
        )