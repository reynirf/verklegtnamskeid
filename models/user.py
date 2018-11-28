class User:
    def __init__(self, name='', user_id=''):
        self.__name = name
        self.__id = user_id
    
    def get_name(self):
        return self.__name
    
    def get_id(self):
        return self.__name

    def __str__(self):
        return "[{}] Welcome {}!".format(self.__id, self.__name)