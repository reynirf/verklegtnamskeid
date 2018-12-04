import sys

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
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN,
                        old_settings)
                return ch
        except:
            import msvcrt
            return msvcrt.getch()

    def getKey(self):
        firstChar = self.get_character()
        if firstChar == '\x1b': # looks like this: ^[
            return {
                '[A': 'up',
                '[B': 'down',
                '[C': 'right',
                '[D': 'left',
                }[self.get_character() + self.get_character()]
        else:
            return firstChar
