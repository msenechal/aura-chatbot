from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from config import OPENAI_API_KEY

def create_llm():
    return OpenAILLM(model_name="o3-mini", model_params={}, api_key=OPENAI_API_KEY)

def create_embedder():
    return OpenAIEmbeddings(model="text-embedding-ada-002", api_key=OPENAI_API_KEY)