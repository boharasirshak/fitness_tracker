import string
import random


def generate_random_password(length: int):
    charset = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choices(charset, k=length))
