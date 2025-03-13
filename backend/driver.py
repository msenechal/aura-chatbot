from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

def create_driver():
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))