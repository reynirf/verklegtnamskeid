class Color:
    COLORS = { # define colors that can be used within this class. 
        "CYAN": "\033[96m",
        "DARKCYAN": "\033[36m",
        "BLUE": "\033[94m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m", 
    }
    END = "\033[0m" # is used to stop the program from rendering text in X color

    def print_colored(self, text, color):
        """ print a string with colored text """
        print("{}{}{}".format(
            self.COLORS[color.upper()],
            text,
            self.END
        ))

    def return_colored(self, text, color):
        """ return a string with colored text """
        return "{}{}{}".format(
            self.COLORS[color.upper()],
            text,
            self.END
        )
