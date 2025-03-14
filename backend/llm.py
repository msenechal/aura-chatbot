from neo4j_graphrag.llm import OpenAILLM
from config import OPENAI_API_KEY

class LLM:

    _instance = None

    def __init__(self, model_name, model_params, api_key):
        self._llm = OpenAILLM(model_name, model_params, api_key)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls("o3-mini", {}, OPENAI_API_KEY)
        return cls._instance
    
    @property
    def llm(self):
        return self._llm
