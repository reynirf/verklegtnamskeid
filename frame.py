import os
from lib.color import Color
class Frame:
    def __init__(self): 
        self.rows, self.columns = os.popen('stty size', 'r').read().split()
        self.logo = """   
    ____    _   _           _          _                 
    | __ )  (_) | |   __ _  | |   ___  (_)   __ _    __ _ 
    |  _ \  | | | |  / _` | | |  / _ \ | |  / _` |  / _` |
    | |_) | | | | | | (_| | | | |  __/ | | | (_| | | (_| |
    |____/  |_| |_|  \__,_| |_|  \___| |_|  \__, |  \__,_|
                                         |___/         
""";

    # os.system('cls' if os.name == 'nt' else 'clear')
    # os.system('while sleep 1;do tput sc;tput cup 0 $(($(tput cols)-11));echo "`date +%r`";tput rc;done &')

    def __str__(self):
        return '{}{}\n'.format(Color.return_colored(self.logo,'yellow'), Color.return_colored('-'*int(self.columns), 'red'))

        
