from neo4j import GraphDatabase
from neo4j_graphrag.message_history import Neo4jMessageHistory
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def create_message_history(session_id=None):
    if session_id is None:
        session_id = str(uuid.uuid4())
        
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    history = Neo4jMessageHistory(
        session_id=session_id,
        driver=driver,
        window=40
    )
    
    return history, driver, session_id