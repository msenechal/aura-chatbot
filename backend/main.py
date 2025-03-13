import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import neo4j
from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.generation import GraphRAG
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.types import RetrieverResultItem
from pydantic import BaseModel, Field
import uvicorn

from chat_history import create_message_history
from config import (NEO4J_URI, 
                    NEO4J_USERNAME, 
                    NEO4J_PASSWORD, 
                    OPENAI_API_KEY, 
                    VECTOR_INDEX_NAME, 
                    ALLOWED_ORIGINS)
from llm import create_llm

api_key = OPENAI_API_KEY

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

llm = create_llm

rag = GraphRAG(retriever=retriever, llm=llm)

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
    session_id: str = None

@app.post("/ask")
def ask_question(request: Request, question: Question):
    try:
        referer = request.headers.get("referer", "")
        if not any(allowed in referer for allowed in ALLOWED_ORIGINS):
            raise HTTPException(status_code=403, detail="Forbidden: Invalid referrer")
        
        history, _, current_session_id = create_message_history(session_id=question.session_id)

        input = question.question
        response = rag.search(
            query_text=input, 
            retriever_config={"top_k": 10}, 
            return_context=True,
            message_history=history
        )
        
        history.add_message({"role": "user", "content": input})
        history.add_message({"role": "assistant", "content": response.answer})
        
        print(f"{question.question}")
        src = []
        for item in response.retriever_result.items:
            src.append(item.metadata)
            
        return {"response": response.answer, "src": src, "session_id": current_session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("shutdown")
def shutdown_event():
    driver.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)