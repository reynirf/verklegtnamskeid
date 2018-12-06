from datetime import datetime
now = datetime.now()

class Vehicle:
    def __init__(self, licence, make, year, type_of_vehicle, color, seats, maintainance):
        self.__licence = licence
        self.__make = make
        self.__year = year
        self.__type_of_vehicle = type_of_vehicle
        self.__color = color
        self.__seats = seats
        self.__maintainance = maintainance
        self.__created = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    
    def __str__(self):
        return "{} {}".format(self.__licence, self.__make)

    def get_licence(self):
        return self.__licence
    
    def get_make(self):
        return self.__make

    def get_vehicle_type(self):
        return self.__type_of_vehicle


