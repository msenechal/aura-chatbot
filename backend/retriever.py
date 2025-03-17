import neo4j
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.types import RetrieverResultItem
from config import VECTOR_INDEX_NAME

class Retriever:
    
    _instance = None

    RETRIEVAL_QUERY = "with node, score OPTIONAL MATCH (node)-[]-(e:__Entity__) return collect(elementId(node))+collect(elementId(e)) as listIds, node.text as nodeText, score"

    def __init__(self, driver, embedder, index_name):
        self._retreiver = VectorCypherRetriever(
            driver,
            index_name=index_name,
            retrieval_query=self.RETRIEVAL_QUERY,
            result_formatter=self.formatter,
            embedder=embedder,
            neo4j_database='neo4j',
        )

    @staticmethod
    def formatter(record: neo4j.Record) -> RetrieverResultItem:
        return RetrieverResultItem(
            content=f'{record.get("nodeText")}: score {record.get("score")}', 
            metadata={"listIds": record.get("listIds")}
        )
    
    @classmethod
    def get_instance(cls,driver, embedder):
        if cls._instance is None:
            cls._instance = cls(driver, embedder, VECTOR_INDEX_NAME)
        return cls._instance
    
    @property
    def retriever(self):
        return self._retreiver


