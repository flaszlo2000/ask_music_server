from uuid import UUID, uuid4


def get_unique_endpoint() -> UUID:
    "Returns unique ids for event endpoints"
    return uuid4() # TODO : check in db first!