from neo4j_graphrag.generation import GraphRAG
from llm import create_llm
from retriever import create_retriever


llm = create_llm
retriever = create_retriever

def create_rag():
    return GraphRAG(retriever=retriever, llm=llm)
