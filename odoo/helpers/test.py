from faker import Faker
from enum import Enum
from helpers.generate import generate_rand_number_from

fake = Faker()

class Password:
    password = "136900"


class AtttributeRandom:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + self.public_name

    def __get__(self, obj, objtype = None):
        if self.public_name == "address":
            return fake.street_address()
        if self.public_name == "state":
            return fake.state()
        if self.public_name == "city":
            return fake.city()
        if self.public_name == "country":
            return fake.country()
        if self.public_name == 'url':
            return fake.url()
    
class GenerateRandomPrice:
    def __get__(self, obj, objtype = None):
        return generate_rand_number_from(1., 1000.)
    
# class Address:
#     address = AtttributeRandom()
#     street = AtttributeRandom()
#     city = AtttributeRandom()
#     address = AtttributeRandom()

class TestData:
    url = AtttributeRandom()
    price = GenerateRandomPrice()
    
    class Vendor:
        # vendor 1
        username1 = "testvendor1"
        email1 = username1 + "@gmail.com"
        
        # vendor 2
        username2 = "testvendor2"
        email2 = username2 + "@yahoo.com"
        
        
        password = Password.password
        
    class User:
        # user 1
        username1 = "testuser1"
        email1 = username1 + "@gmail.com"
        
        # user 2
        username2 = "testuser2"
        email2 = username2 + "@microsoft.com"
        
        password = Password.password
        
    class Address:
        address = AtttributeRandom()
        city = AtttributeRandom()
        state = AtttributeRandom()
        country = AtttributeRandom()
        
    class ProductCateory:
        class Hardware:
            name = "Hardware"
            description = "Vendor selling hardware items"
            active = True
        
        class Cloth:
            name = "Cloth"
            description = "Vendor selling Cloths"
            active = True
            
        class Shirt:
            name = "Shirt"
            description = "Vendor selling shirt, clothing item"
            active = True
        
        class Lock:
            name = "Lock"
            description = "Vendor selling Lock"
            active = True
        
        class WheelLock:
            name = "Wheel lock"
            description = "Vendor selling wheel lock (a type of lock)"
            active = True
            
        class DoorLock:
            name = "Door lock"
            description = "Vendor selling Door lock (a type of lock)"
            
        class WheelChainLock:
            name = "Wheel chain lock"
            description = "Vendor selling chain wheel lock (a type of lock and wheel lock)"
            
    class Attribute:
        class Color(Enum):
            RED = 1, 'Red'
            BROWN = 2, "Brown"
            GOLDEN = 3, "Golden"
            SILVER = 4, "Silve"
            BLACK = 5, "Black"
            
        class ClothSize(Enum):
            SMALL = 1, "Small"
            MEDIUM = 2, "Medium"
            LARGE = 3, "Large"
        
        class Measurement(Enum):
            CM = 1, "Centimeter"
            M = 2, "Meter"
            KM = 3, "Kilometer"