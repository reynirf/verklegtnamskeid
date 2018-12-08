from datetime import date


class Vehicle:
    def __init__(self, licence, make, model, year, type_of_vehicle,
                 seats, fuel, transmission, maintainance=0, dates=[]):
        self.__licence = licence
        self.__make = make
        self.__model = model
        self.__year = year
        self.__type_of_vehicle = type_of_vehicle
        self.__seats = seats
        self.__fuel = fuel
        self.__transmission = transmission
        self.__maintainance = maintainance
        self.__rented_dates = []
        self.set_rented_dates(dates)
        self.set_price()

    def set_price(self):
        if self.__type_of_vehicle == "small car":
            self.__price_per_day = 9000
        elif self.__type_of_vehicle == "sedan":
            self.__price_per_day = 10000
        elif self.__type_of_vehicle == "offroad":
            self.__price_per_day = 12000
        elif self.__type_of_vehicle == "bus":
            self.__price_per_day = 13000

    def set_rented_dates(self, dates):
        try:
            for d in dates:
                year = d[:4]
                month = d[5:7]
                day = d[8:]
                self.__rented_dates.append(date(int(year), int(month), int(day)))
        except ValueError:
            pass

    def get_rented_dates(self):
        return self.__rented_dates

    def __str__(self):
        return "{} {}".format(self.__licence, self.__make)

    def get_licence(self):
        return self.__licence

    def get_make(self):
        return self.__make

    def get_vehicle_type(self):
        return self.__type_of_vehicle

    def get_price_per_day(self):
        return self.__price_per_day

    def get_attributes(self):
        return self.__licence, self.__make, self.__model, self.__year, self.__type_of_vehicle, self.__seats, self.__fuel, self.__transmission, self.__maintainance
