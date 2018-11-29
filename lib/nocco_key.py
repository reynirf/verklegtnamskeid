import termios, sys, tty

class NoccoKey:
        def get():
                try:
                        def get_character():
                                fd = sys.stdin.fileno()
                                old_settings = termios.tcgetattr(fd)
                                try:
                                        tty.setraw(fd)
                                        ch = sys.stdin.read(1)
                                finally:
                                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                                        return ch

                        def getKey():
                                firstChar = get_character()
                                if firstChar == '\x1b':
                                        return {"[A": "up", "[B": "down", "[C": "right", "[D": "left"}[get_character() + get_character()]
                                else:
                                        return firstChar

                        return getKey()
                except:
                        pass