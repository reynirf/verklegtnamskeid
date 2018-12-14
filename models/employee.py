from lib.color import Color


class Employee:
    """An employee has:
        title: str
        name: str
        user_id: str
        password: str
    """
    def __init__(self, title="", name="", user_id="", password=""):
        self.__title = title
        self.__name = name
        self.__id = user_id
        self.__password = password
        self.color = Color()
    
    def get_name(self):
        return self.__name
    
    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def __str__(self):
        return "[{}] {}. {}".format(
            self.color.return_colored(self.__id, "yellow"),
            self.color.return_colored(self.__title, "bold"), 
            self.color.return_colored(self.__name,"bold")
        )