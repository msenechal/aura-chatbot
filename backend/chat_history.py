from neo4j import GraphDatabase
from neo4j_graphrag.message_history import Neo4jMessageHistory
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

def create_message_history(session_id=None):

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    
    history = Neo4jMessageHistory(
        session_id=session_id,
        driver=driver,
        window=40
    )
    
    return history, driver, session_id