from enum import Enum, auto


class Services(Enum):
    ADD_DOCUMENT = auto()
    QUERY_DB = auto()
    QUERY_MEMORY = auto()
