from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class Neo4jDriver:
    
    # singleton instance, so only one driver instance created and used through app
    _instance = None

    def __init__(self, uri, username, password):
        self._driver = GraphDatabase.driver(uri, auth=(username, password))

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
        return cls._instance

    @property
    def driver(self):
        return self._driver
    
    def close(self):
        if hasattr(self, '_driver') and self._driver:
            self._driver.close()