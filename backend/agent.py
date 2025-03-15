from neo4j_graphrag.generation import GraphRAG
from llm import LLM
from retriever import create_retriever


llm = LLM.get_instance().llm
retriever = create_retriever

def create_rag():
    return GraphRAG(retriever=retriever, llm=llm)
