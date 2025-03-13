from neo4j_graphrag.message_history import Neo4jMessageHistory
from driver import create_driver

def create_message_history(session_id=None):

    driver = create_driver
    
    history = Neo4jMessageHistory(
        session_id=session_id,
        driver=driver,
        window=40
    )
    
    return history, driver, session_id