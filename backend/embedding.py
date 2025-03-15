from neo4j_graphrag.embeddings import OpenAIEmbeddings
from config import OPENAI_API_KEY

class Embedding:

    _instance = None

    def __init__(self, model, api_key):
        self._embedder = OpenAIEmbeddings(model, api_key)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls("text-embedding-ada-002", OPENAI_API_KEY)
        return cls._instance
    
    @property
    def embedder(self):
        return self._embedder
      