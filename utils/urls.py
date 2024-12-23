import string
import random


def generate_short_id(length=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length)).lower()
