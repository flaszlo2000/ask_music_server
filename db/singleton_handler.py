from typing import Optional

from db.main import BaseDbHandler

__db_handler: Optional[BaseDbHandler] = None # NOTE: real singletion in future?

def global_db_handler(setup: Optional[BaseDbHandler] = None) -> BaseDbHandler:
    global __db_handler

    if __db_handler is None:
        if setup is None:
            raise AttributeError("Global db handler hasn't been set yet")
        __db_handler = setup
    
    return __db_handler