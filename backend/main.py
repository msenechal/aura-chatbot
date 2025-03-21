import uvicorn

from config import (
    NEO4J_URI, 
    NEO4J_USERNAME, 
    NEO4J_PASSWORD,
    OPENAI_API_KEY,
    VECTOR_INDEX_NAME,
    ALLOWED_ORIGINS
)

from driver import Neo4jDriver
from embedding import Embedding
from retriever import Retriever
from llm import LLM
from chat_history import MessageHistory
from agent import Agent
from api import API
from routes import Routes

driver_instance = Neo4jDriver.get_instance(
    uri=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD
)

driver = driver_instance.driver

embedder_instance = Embedding.get_instance(
    api_key=OPENAI_API_KEY
)

embedder = embedder_instance.embedder

retriever_instance = Retriever.get_instance(
    driver=driver, 
    embedder=embedder,
    index_name=VECTOR_INDEX_NAME
)

retriever = retriever_instance.retriever

llm_instance = LLM.get_instance(
    api_key=OPENAI_API_KEY
)

llm = llm_instance.llm

agent_instance = Agent.get_instance(
    retriever=retriever, 
    llm=llm
)

rag = agent_instance.rag

message_history = MessageHistory(
    driver=driver
)

api_instance = API.get_instance(
    allowed_origins=ALLOWED_ORIGINS
)

app = api_instance.app

routes = Routes(
    app=app, 
    rag=rag, 
    message_history=message_history, 
    allowed_origins=ALLOWED_ORIGINS
)

@app.on_event("shutdown")
def shutdown_event():
    driver.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)