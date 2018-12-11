class Customer:
    def __init__(self, name, ssn, birthday, phone, email, 
        address, driver_license, credit_card):
        self.__name = name
        self.__ssn = ssn
        self.__birthday = birthday
        self.__phone = phone
        self.__email = email
        self.__address = address
        self.__driver_license = driver_license
        self.__credit_card = credit_card
        self.__orders = []

    def __str__(self):
        return '{} | {}'.format(self.__name, self.__ssn)

    def get_ssn(self):
        return self.__ssn

    def return_details(self):
        return {
            "Name": self.__name,
            "SSN": self.__ssn,
            "Birthday": self.__birthday,
            "Phone number": self.__phone,
            "Email address": self.__email,
            "Home address": self.__address,
            "Driver license category": self.__driver_license,
            "Credit card number": self.__credit_card
        }
