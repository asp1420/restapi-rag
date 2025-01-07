from typing import Final


TITLE: Final[str] = 'REST-API RAG LLM'
DESCRIPTION: Final[str] = (
    'This API, developed using FastAPI, is designed to retrieve answers based on user queries and a context. '
    'The responses are sourced either from LLM model utilizing FAISS when documents are available. '
    )
DOC_ANSWER: Final[str] = 'Answer based on user query.'
DOC_ANSWER_RESPONSE: Final[str] = 'Response of REST-API.'
DOC_ADD_COLLECTION: Final[str] = 'Add a document file to the FAISS DB.'
DOC_ASWER_DETAILS: Final[str] = 'Message that indicates error messages found during the execution.'
DOC_QUERY_DB: Final[str] = 'Create a response from a user query based on LLM model.'