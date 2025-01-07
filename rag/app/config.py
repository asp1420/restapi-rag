import os

from dataclasses import dataclass, field

CONF_TYPE = str | None
CONF_VARIABLES = {
    'APP_VERSION': os.environ.get('APP_VERSION', '0.1'),
    'LLM_MODEL': os.environ.get('LLM_MODEL', 'meta-llama/Llama-3.2-1B-Instruct'),
    'EMBEDDING_MODEL': os.environ.get('EMBEDDING_MODEL', 'nomic-ai/nomic-embed-text-v1.5'),
    'HF_TOKEN': os.environ.get('HF_TOKEN', None),
    'OPENAI_API_KEY': os.environ.get('OPENAI_API_KEY', None)
}


@dataclass
class Configuration:
    config: dict[str, str | None] = field(default_factory=lambda: CONF_VARIABLES)

    def get_property(self, property_name: str) -> CONF_TYPE:
        if property_name not in self.config.keys():
            return None
        return self.config[property_name]


@dataclass
class OpenAPISchemaConfig(Configuration):

    @property
    def version(self) -> CONF_TYPE:
        return self.get_property('APP_VERSION')


@dataclass
class LLMConfig(Configuration):

    @property
    def chat_model(self) -> CONF_TYPE:
        return self.get_property('LLM_MODEL')
    
    @property
    def embedding_model(self) -> CONF_TYPE:
        return self.get_property('EMBEDDING_MODEL')

    @property
    def hugging_token(self) -> CONF_TYPE:
        return self.get_property('HF_TOKEN')

    @property
    def openai_token(self) -> CONF_TYPE:
        return self.get_property('OPENAI_API_KEY')
