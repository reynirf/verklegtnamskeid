class Price:
    """This class holds all the information about the prices of the vehicles,
    by separating vehicles in different categories and calculates the final price
    after adding the insurance on top of the initial price.
    All cars must be with basic insurance, and then it is up to the customer to choose
    if he/she wants to add extra/kasko insurance or not.
    """
    def __init__(self):
        self.__vehicle_types = ["Small car", "Sedan", "Offroad", "Bus"]

    def get_price(self, vehicle_type):
        if vehicle_type == "smallcar":
            self.price_per_day = 9000
        elif vehicle_type == "sedan":
            self.price_per_day = 10000
        elif vehicle_type == "offroad":
            self.price_per_day = 12000
        else:
            self.price_per_day = 13000
        return self.price_per_day
    
    def get_insurance(self, vehicle_type):
        if vehicle_type == "smallcar":
            self.extra_insurance = 1050
        elif vehicle_type == "sedan":
            self.extra_insurance = 1150
        elif vehicle_type == "offroad":
            self.extra_insurance = 1350
        else:
            self.extra_insurance = 1500  
        return self.extra_insurance      

    def print_prices(self, vehicle_type):
        price = self.get_price(vehicle_type)
        basic_ins = int(price * 0.35)
        extra_ins = self.get_insurance(vehicle_type)
        if vehicle_type == "smallcar":
            vehicle_type = "small car"
        return "{:<15}{:>12}{:>20}{:>20}".format(vehicle_type.capitalize(), price, basic_ins, extra_ins)