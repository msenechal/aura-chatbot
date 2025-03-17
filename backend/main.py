import uvicorn

from config import (OPENAI_API_KEY)
from driver import Neo4jDriver
from embedding import Embedding
from retriever import Retriever
from api import create_api


api_key = OPENAI_API_KEY
driver = Neo4jDriver.get_instance().driver
embedder = Embedding.get_instance().embedder
retriever = Retriever.get_instance(driver=driver, embedder=embedder).retriever

@app.on_event("shutdown")
def shutdown_event():
    driver.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)