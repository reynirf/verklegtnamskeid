from lib.color import Color

class Employee:
    def __init__(self, name='', user_id='', password=''):
        self.__name = name
        self.__id = user_id
        self.__password = password
        self.color = Color()
    
    def get_name(self):
        return self.__name
    
    def get_id(self):
        return self.__name

    def __str__(self):
        return "[{}] {}".format(
            self.color.return_colored(self.__id, 'yellow'), 
            self.color.return_colored(self.__name,'bold')
        )