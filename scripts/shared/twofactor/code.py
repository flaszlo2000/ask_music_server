from random import choice
from uuid import uuid4


def get_secure_code() -> str:
    uuid_segments = str(uuid4()).split('-')

    return uuid_segments[0] + choice(uuid_segments[1:-1])

# def generate_code() -> str:...