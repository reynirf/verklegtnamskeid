from datetime import datetime
now = datetime.now()

class Vehicle:
    def __init__(self,color):
        self.color = color
        self.created = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
    
    def __str__(self):
        return "JUST TESTING"


