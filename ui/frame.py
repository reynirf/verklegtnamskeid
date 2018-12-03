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
        self.rows, self.columns = os.popen('stty size', 'r').read().split()
        self.logo = """  
     ____    _   _           _          _                 
    | __ )  (_) | |   __ _  | |   ___  (_)   __ _    __ _ 
    |  _ \  | | | |  / _` | | |  / _ \ | |  / _` |  / _` |
    | |_) | | | | | | (_| | | | |  __/ | | | (_| | | (_| |
    |____/  |_| |_|  \__,_| |_|  \___| |_|  \__, |  \__,_|
                                            |___/             
""";

    # os.system('while sleep 1;do tput sc;tput cup 0 $(($(tput cols)-11));echo "`date +%r`";tput rc;done &')

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

    def __str__(self):
        return '{}{}\n'.format(
            self.color.return_colored(self.logo,'bold'),
            self.color.return_colored('-'*int(self.columns), 'bold')
        )