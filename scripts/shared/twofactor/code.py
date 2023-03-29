from random import choice
from uuid import uuid4

from scripts.shared.twofactor.code_handler import Code


def get_secure_code() -> Code:
    uuid_segments = str(uuid4()).split('-')

    return Code(uuid_segments[0] + choice(uuid_segments[1:-1]))

# def generate_code() -> str:...