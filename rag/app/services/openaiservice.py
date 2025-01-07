from dataclasses import dataclass, field
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableBinding
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from .service import Service
from ..config import LLMConfig
from ..utils.llm import create_prompt


@dataclass
class OpenAIService(Service):
    collection: str = field(default_factory=str)
    db: FAISS = field(init=False, default=None)
    llm: ChatOpenAI = field(init=False, default=None)
    config: LLMConfig = field(init=False, default_factory= lambda : LLMConfig())

    def __post_init__(self) -> None:
        embedding = self._load_embedding()
        self.db = self._load_database(embedding=embedding)
        self.llm = self._load_llmchat()

    def format_docs(self, docs):
        content = "\n\n".join([d.page_content.replace('\t', ' ') for d in docs])
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
        return {'answer': data}

    def _load_llmchat(self) -> ChatOpenAI:
        return ChatOpenAI(model=self.config.chat_model)
