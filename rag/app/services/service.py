from dataclasses import dataclass, field
from abc import ABC
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from ..utils.logger import Logger
from ..consts.paths import PERSIST_DIRECTORY
from ..exceptions.app import CollectionNotFound
from typing import Any


@dataclass
class Service(ABC):

    data: Any = field(default=None)
    _data: Any = field(init=False, repr=False)

    @property
    def data(self) -> Any:
        return self._data

    @data.setter
    def data(self, data: Any) -> None:
        self._data = data

    def format_response(self, data: Any) -> Any:
        return data

    def execute(self) -> dict[str, Any]:
        preprocessed = self.preprocess(data=self.data)
        processed = self.process(data=preprocessed)
        postprocessed = self.postprocess(data=processed)
        result = self.format_response(data=postprocessed)
        return result

    def preprocess(self, data: Any | None) -> Any | None:
        return data

    def process(self, data: Any | None) -> Any | None:
        return data

    def postprocess(self, data: Any | None) -> Any | None:
        return data

    def _load_llmchat(self)  -> Any | None: ...

    def _load_embedding(self) -> HuggingFaceEmbeddings:
        Logger.info('Loading embedding models ⏳ ...')
        embedding = HuggingFaceEmbeddings(
            model_name=self.config.embedding_model,
            model_kwargs={'trust_remote_code': True},
            encode_kwargs={'normalize_embeddings': False}
        )
        Logger.info('Loaded embedding ✅')
        return embedding

    def _load_database(self, embedding: HuggingFaceEmbeddings) -> FAISS:
        Logger.info('Loading database ⏳ ...')
        db = None
        try:
            db = FAISS.load_local(
                folder_path=PERSIST_DIRECTORY,
                embeddings=embedding,
                index_name=self.collection,
                allow_dangerous_deserialization=True
            )
            Logger.info('Loaded vector database ✅')
        except RuntimeError:
            raise CollectionNotFound(self.collection)
        return db
