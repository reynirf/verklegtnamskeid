import sys
import os


class NoccoKey:
    def __init__(self):
        pass

    def get(self):
        return self.getKey()

    def get_character(self):
        try:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return char
        except ModuleNotFoundError: # for Windows
            import msvcrt
            firstChar = msvcrt.getch()
            if firstChar == b'\xe0':
                return {b'H': 'up', b'P': 'down', b'M': 'right', b'K': 'left'}[msvcrt.getch()]
            else:
                return firstChar

    def getKey(self):
        firstChar = self.get_character()
        if firstChar == '\x1b':  # looks like this: ^[
            return {
                '[A': 'up',
                '[B': 'down',
                '[C': 'right',
                '[D': 'left',
            }[self.get_character() + self.get_character()]
        else:
            return firstChar
