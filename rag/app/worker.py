from .utils.logger import Logger
from .exceptions.app import (
    InvalidFile,
    CollectionNotFound,
    DocumentNotAdded,
    APIKeyNotSet
)
from .utils.documents import extract
from .processors.docprocessor import DocumentProcessor
from .consts.stypes import Services


def process_data(
        service: Services,
        data_bytes: str=None,
        data_type: str=None,
        filename: str=None,
        collection: str=None
    ):
    details = None
    response = -1
    try:
        data = extract(data_bytes=data_bytes, data_type=data_type)
        processor = DocumentProcessor(
            service=service, data=data, filename=filename,
            collection=collection
        )
        processor.run()
        response = processor.get()
    except (InvalidFile, CollectionNotFound, DocumentNotAdded, APIKeyNotSet) as exc:
        details = str(exc)
        Logger.error(details + ' ❌')
    except Exception as exc:
        details = str(exc)
        Logger.error(details)
    return response, details
