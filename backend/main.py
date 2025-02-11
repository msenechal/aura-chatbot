from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.retrievers import VectorCypherRetriever
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import neo4j
from neo4j_graphrag.types import RetrieverResultItem
import os
from dotenv import load_dotenv

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
VECTOR_INDEX_NAME = os.getenv("VECTOR_INDEX_NAME")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS")

api_key = os.getenv("OPENAI_API_KEY")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

embedder = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key)

def formatter(record: neo4j.Record) -> RetrieverResultItem:
    return RetrieverResultItem(content=f'{record.get("nodeText")}: score {record.get("score")}', metadata={"listIds": record.get("listIds")})

RETRIEVAL_QUERY = "with node, score OPTIONAL MATCH (node)-[]-(e:__Entity__) return collect(elementId(node))+collect(elementId(e)) as listIds, node.text as nodeText, score"
retriever = VectorCypherRetriever(
    driver,
    index_name=VECTOR_INDEX_NAME,
    retrieval_query=RETRIEVAL_QUERY,
    result_formatter=formatter,
    embedder=embedder,
    neo4j_database='neo4j',
)

llm = OpenAILLM(model_name="o3-mini", model_params={}, api_key=api_key)

rag = GraphRAG(retriever=retriever, llm=llm)

driver.close()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_question(question: Question):
    try:
        input = question.question
        response = rag.search(query_text=input, retriever_config={"top_k": 3}, return_context=True)
        src = []
        for item in response.retriever_result.items:
            src.append(item.metadata)
        return {"response": response.answer, "src": src}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

uvicorn.run(app, host="0.0.0.0", port=8001)