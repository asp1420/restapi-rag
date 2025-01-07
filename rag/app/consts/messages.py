from typing import Final


BAD_PARAMETER_REQUEST: Final[str] = "@document param not sent in request."
INVALID_FILE: Final[str] = "The file is not supported for this REST API."
INVALID_FORMAT_FILE: Final[str] = "The input file doesn't contain a valid image format."
DOCUMENT_NOT_ADDED: Final[str] = "The document with file name {} was found in the data base, so it was not added to the data base."
SERVICE_APIKEY_NOT_SET: Final[str] = 'The Service API Key is not configured. Please set either HF_TOKEN or OPENAI_API_KEY in the .env file.'

DOCUMENT_ADDED: Final[str] = "The document was added to the data base."
INVALID_COLLECTION: Final[str] = 'The collection "{}" does not exist.'