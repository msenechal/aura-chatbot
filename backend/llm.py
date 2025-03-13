from neo4j_graphrag.llm import OpenAILLM
from config import OPENAI_API_KEY

def create_llm():
    OpenAILLM(model_name="o3-mini", model_params={}, api_key=OPENAI_API_KEY)