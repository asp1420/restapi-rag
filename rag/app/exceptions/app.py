from ..consts import messages


class InvalidFile(Exception):
    def __init__(self) -> None: ...

    def __str__(self) -> str:
        return messages.INVALID_FILE


class InvalidCollectionName(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class CollectionNotFound(Exception):
    def __init__(self, collection: str) -> None:
        self.collection = collection

    def __str__(self):
        return messages.INVALID_COLLECTION.format(self.collection)


class DocumentNotAdded(Exception):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __str__(self):
        return messages.DOCUMENT_NOT_ADDED.format(self.filename)


class APIKeyNotSet(Exception):
    def __init__(self) -> None: ...

    def __str__(self):
        return messages.SERVICE_APIKEY_NOT_SET