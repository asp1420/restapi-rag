from pydantic import BaseModel, Field
from ..consts.api import (
    DOC_ANSWER,
    DOC_ANSWER_RESPONSE,
    DOC_ASWER_DETAILS
)


class RAGResponse(BaseModel):
    answer: str = Field(description=DOC_ANSWER)


class RequestResponse(BaseModel):
    response: RAGResponse | int | None = Field(default=None, description=DOC_ANSWER_RESPONSE)
    details: str | None = Field(default=None, description=DOC_ASWER_DETAILS)
