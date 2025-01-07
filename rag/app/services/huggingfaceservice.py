from dataclasses import dataclass, field
from langchain_community.vectorstores import FAISS
from langchain_huggingface import (
    HuggingFaceEmbeddings,
    ChatHuggingFace,
    HuggingFacePipeline
)
from langchain_core.runnables import RunnableBinding
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from .service import Service
from ..config import LLMConfig
from ..utils.llm import create_prompt
from ..utils.logger import Logger
from ..consts.paths import PERSIST_DIRECTORY
from ..exceptions.app import CollectionNotFound


@dataclass
class HuggingFaceService(Service):
    collection: str = field(default_factory=str)
    db: FAISS = field(init=False, default=None)
    llm: ChatHuggingFace = field(init=False, default=None)
    config: LLMConfig = field(init=False, default_factory= lambda : LLMConfig())

    def __post_init__(self) -> None:
        embedding = self._load_embedding()
        self.llm = self._load_llmchat()
        self.db = self._load_database(embedding=embedding)

    def format_docs(self, docs):
        content = "\n\n".join([doc.page_content.replace('\t', ' ') for doc in docs])
        return content

    def preprocess(self, data: None) -> RunnableBinding:
        retriever = self.db.as_retriever(search_kwargs={'k': 4})
        prompt = create_prompt()
        chain = (
            {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return chain

    def process(self, data: RunnableBinding) -> str:
        output = data.invoke(self.data)
        return output

    def format_response(self, data: str) -> dict[str, str]:
        answer = None
        # The following response process is due to a bug with
        # ChatHuggingFace and LangChain. This may be resolved 
        # in a future version.
        pos = data.rfind('<|end_header_id|>')
        if pos != -1:
            answer = data[pos:]
            answer = answer.replace('<|end_header_id|>', '')
        return {'answer': answer}

    def _load_llmchat(self) -> ChatHuggingFace:
        Logger.info('Loading LLM Chat model ⏳ ...')
        pipeline_kwargs = {
            "max_new_tokens": 2000,
            "top_p": 0.8,
            "temperature": 0.1,
            "repetition_penalty": 1.1,
        }
        pipeline = HuggingFacePipeline.from_model_id(
            model_id=self.config.chat_model,
            task="text-generation",
            device=0,
            pipeline_kwargs=pipeline_kwargs,
        )
        llm = ChatHuggingFace(llm=pipeline)
        llm.llm.pipeline.tokenizer.pad_token_id = llm.llm.pipeline.tokenizer.eos_token_id
        Logger.info('Loaded LLM Chat model ✅')
        return llm