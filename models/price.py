class Price:
    def get_price(self, vehicle_type):
        if vehicle_type == 'smallcar':
            self.price_per_day = 9000
        elif vehicle_type == 'sedan':
            self.price_per_day = 10000
        elif vehicle_type == 'offroad':
            self.price_per_day == 12000
        else:
            self.price_per_day = 13000
        return self.price_per_day
    
    def get_insurance(self, vehicle_type):
        if vehicle_type == 'smallcar':
            self.extra_insurance = 1050
        elif vehicle_type == 'sedan':
            self.extra_insurance = 1150
        elif vehicle_type == 'offroad':
            self.extra_insurance = 1350
        else:
            self.extra_insurance = 1500  
        return self.extra_insurance      