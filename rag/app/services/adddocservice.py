import os

from dataclasses import dataclass, field
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from .service import Service
from ..config import LLMConfig
from ..consts.paths import DOCUMENT_DIRECTORY, PERSIST_DIRECTORY 
from ..consts.messages import DOCUMENT_ADDED
from ..exceptions import app
from ..utils.logger import Logger
from io import BytesIO


@dataclass
class AddDocumentService(Service):
    filename: str = field(default_factory=str)
    collection: str = field(default_factory=str)
    embedding: HuggingFaceEmbeddings = field(init=False, default=None)

    def __post_init__(self) -> None:
        config = LLMConfig()
        self.embedding = HuggingFaceEmbeddings(
            model_name=config.embedding_model,
            model_kwargs={'trust_remote_code': True},
            encode_kwargs={'normalize_embeddings': False}
        )
        Logger.info('Created embedding and database ✅')

    def preprocess(self, data: BytesIO) -> None:
        os.makedirs(DOCUMENT_DIRECTORY, exist_ok=True)
        with open(os.path.join(DOCUMENT_DIRECTORY, self.filename), 'wb') as ptr:
            ptr.write(data.getbuffer())

    def process(self, data: None) -> None:
        Logger.info(f'Adding document {self.filename} to the vector database ⏳')
        try:
            loader = DirectoryLoader(path=DOCUMENT_DIRECTORY)
            documents = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents=documents)
            db = FAISS.from_documents(documents=chunks, embedding=self.embedding)
            db.save_local(folder_path=PERSIST_DIRECTORY, index_name=self.collection)
            Logger.info(f'Successfully added to vector database ✅')
        except ValueError as e:
            raise app.InvalidCollectionName(str(e))

    def postprocess(self, data: None) -> None:
        Logger.info('Cleaning up 🧹')
        os.remove(os.path.join(DOCUMENT_DIRECTORY, self.filename))

    def format_response(self, data: None) -> dict[str, str]:
        return {'answer': DOCUMENT_ADDED}
