class Customer:
    """Customer has:
        name: str
        ssn: int
        phone: int
        email: str
        address: str
        driver_liccence: str
        credit_card: int
    """
    def __init__(self, name, ssn, phone, email, address, driver_license, credit_card):
        self.__name = name
        self.__ssn = ssn
        self.__phone = phone
        self.__email = email
        self.__address = address
        self.__driver_license = driver_license
        self.__credit_card = credit_card
        self.__orders = []

    def __str__(self):
        formatted_ssn = "{}-{}".format(self.__ssn[:6], self.__ssn[6:])
        return "{} | {}".format(self.__name, formatted_ssn)

    def get_ssn(self):
        return self.__ssn

    def return_details(self):
        """ Returns customer details in a dictionary """
        return {
            "Name": self.__name,
            "SSN": self.__ssn,
            "Phone number": self.__phone,
            "Email address": self.__email,
            "Home address": self.__address,
            "Driver license category": self.__driver_license,
            "Credit card number": self.__credit_card
        }
