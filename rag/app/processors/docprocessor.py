from dataclasses import dataclass, field
from ..processors.processor import Processor
from ..consts.stypes import Services
from ..factories.servicefactory import ServiceFactory
from ..utils.logger import Logger
from io import BytesIO
from typing import Any


@dataclass
class DocumentProcessor(Processor):

    service: Services
    data: BytesIO
    filename: str = field(default_factory=str)
    collection: str = field(default_factory=str)
    result: dict[str, Any] = field(init=False, default_factory=dict)

    def run(self) -> None:
        Logger.info('Processing request ⚙️ ...')
        service = ServiceFactory.create(
            stype=self.service, data=self.data, filename=self.filename,
            collection=self.collection
        )
        self.result = service.execute()
        Logger.info(f'Process {self.service.name} completed! ✅')

    def get(self) -> Any:
        return self.result
