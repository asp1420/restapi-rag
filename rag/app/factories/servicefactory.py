from ..consts.stypes import Services
from ..utils.logger import Logger
from ..services import (
    AddDocumentService,
    HuggingFaceService,
    OpenAIService
)
from ..config import LLMConfig
from ..exceptions.app import APIKeyNotSet
from typing import Any


class ServiceFactory:

    @staticmethod
    def create(stype: Services, data: Any, filename: str, collection: str):
        service = None
        config = LLMConfig()
        match stype:
            case Services.ADD_DOCUMENT:
                service = AddDocumentService(data=data, filename=filename, collection=collection)
            case Services.QUERY_DB:
                if config.openai_token:
                    service = OpenAIService(data=data, collection=collection)
                elif config.hugging_token:
                    service = HuggingFaceService(data=data, collection=collection)
                else:
                    raise APIKeyNotSet
        Logger.info(f'Created service {stype.name} ✅')
        return service
