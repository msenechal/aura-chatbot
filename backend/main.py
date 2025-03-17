import uvicorn

from config import (OPENAI_API_KEY)
from driver import Neo4jDriver
from embedding import Embedding
from retriever import Retriever
from chat_history import MessageHistory
from api import create_api


api_key = OPENAI_API_KEY
driver_instance = Neo4jDriver.get_instance()
driver = driver_instance.driver
embedder_instance = Embedding.get_instance()
embedder = embedder_instance.embedder
retriever_instance = Retriever.get_instance(driver=driver, embedder=embedder)
retriever = retriever_instance.retriever

message_history = MessageHistory(driver=driver)

@app.on_event("shutdown")
def shutdown_event():
    driver.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)