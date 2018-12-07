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
                termios.tcsetattr(fd, termios.TCSADRAIN,
                                  old_settings)
                return char
        except ModuleNotFoundError:
            import msvcrt
            while 1:
                if msvcrt.kbhit():
                    msvcrt.getch()
                    char = msvcrt.getch()
                    vals = [72, 77, 80, 75]
                    try:
                        return vals.index(ord(char.decode('utf-8')))
                    except ValueError:
                        return ord(char.decode('utf-8'))

    def getKey(self):
        firstChar = self.get_character()
        if firstChar == '\x1b':  # looks like this: ^[
            return {

                '[A': 'up',
                '[B': 'down',
                '[C': 'right',
                '[D': 'left',
            }[self.get_character() + self.get_character()]
        elif os.name == 'nt':
            if firstChar == 0:
                return 'up'
            elif firstChar == 1:
                return 'right'
            elif firstChar == 2:
                return 'down'
            elif firstChar == 3:
                return 'left'
            elif firstChar == 13:
                return 'enter'
            else:
                return firstChar
        else:
            return firstChar
