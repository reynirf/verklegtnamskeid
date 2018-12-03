class Color:
    COLORS = {
        'CYAN':'\033[96m',
        'DARKCYAN':'\033[36m',
        'BLUE':'\033[94m',
        'GREEN':'\033[92m',
        'YELLOW':'\033[93m',
        'RED':'\033[91m',
        'BOLD':'\033[1m',
        'UNDERLINE':'\033[4m',
        'END':'\033[0m'
    }   

    def __init__(self):
        pass

    def print_colored(self, text, color):
        print('{}{}{}'.format(
            self.COLORS[color.upper()],
            text,
            self.COLORS['END']
        ))
        
    def return_colored(self, text, color):
        return '{}{}{}'.format(
            self.COLORS[color.upper()],
            text,
            self.COLORS['END']
        )
