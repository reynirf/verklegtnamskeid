import sys
import os

class NoccoKey:

    def __init__(self):
        self.msvcrt = ""

    def get_character(self):
        """ get character input from user """
        try: # Unix
            # only accessible for unix devices
            import termios 
            import tty
            fd = sys.stdin.fileno() 
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1) # read 1 character
            finally:
                # set system instruction on how to get char
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 
                return char
        except ModuleNotFoundError: # Windows
            import msvcrt
            self.msvcrt = msvcrt # to use the module in getKey function
            firstChar = msvcrt.getch() # get character that use presses
            return firstChar

    def getKey(self):
        """ 
            format character to key if special key was pressed and return it, 
            else return character unchanged 
        """ 
        firstChar = self.get_character()
        # if statement for Unix
        if firstChar == "\x1b":  # looks like this: ^[
            return {
                "[A": "up", # \x1b[A
                "[B": "down",
                "[C": "right",
                "[D": "left",
            }[self.get_character() + self.get_character()]
        # elif for Windows
        elif firstChar == b"\xe0": # if special key is pressed, for instance arrow keys
            # return "up" if Windows version of arrow key "up" is b"\xe0H etc...
            return {
                b"H": "up", 
                b"P": "down", 
                b"M": "right", 
                b"K": "left"
            }[self.msvcrt.getch()]
        # else
        return firstChar
