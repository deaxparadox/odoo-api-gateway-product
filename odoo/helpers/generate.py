from random import randint
from uuid import uuid4
import string
import random

char_pool = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase

def generate_uuid4():
    return str(uuid4())

def generate_rand_number_from(a: int | float, b:int | float, /):
    if isinstance(a, int) and isinstance(b, int):
        return float(randint(a, b))
    elif isinstance(a, float) and isinstance(b, float):
        return float(randint(int(b), int(b)))
    else:
        # (isinstance(a, int) or isinstance(b, float) or (isinstance(a, float) or isinstance(b, int)))
        return float(randint(int(a), int(b)))

def generate_random_string(length: int = 10):
    return "".join(random.sample(char_pool * 100, length))