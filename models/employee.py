class Employee:
    def __init__(self, name='', user_id='', password=''):
        self.__name = name
        self.__id = user_id
        self.__password = password
    
    def get_name(self):
        return self.__name
    
    def get_id(self):
        return self.__name

    def __str__(self):
        return "[{}] Welcome {}!".format(self.__id, self.__name)