import sys,tty,termios
class NoccoKey:
        def __call__(self):
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                        tty.setraw(sys.stdin.fileno())
                        ch = sys.stdin.read(3)
                finally:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                return ch

        def get():
                inkey = NoccoKey()
                k = inkey()
                # while 1:
                #         k=inkey()
                #         if k!='':break
                if k =='\x1b[A':
                        k = 'up'
                elif k =='\x1b[B':
                        k = 'down'
                # elif k=='\x1b[C':
                #         # print ("right")
                #         pass
                # elif k=='\x1b[D':
                #         # print ("left")
                #         pass
                else:
                        k = 0
                return k
