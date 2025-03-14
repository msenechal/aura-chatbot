import neo4j
from neo4j_graphrag.retrievers import VectorCypherRetriever
from neo4j_graphrag.types import RetrieverResultItem
from config import VECTOR_INDEX_NAME
from driver import create_driver
from llm import create_embedder


RETRIEVAL_QUERY = "with node, score OPTIONAL MATCH (node)-[]-(e:__Entity__) return collect(elementId(node))+collect(elementId(e)) as listIds, node.text as nodeText, score"


def formatter(record: neo4j.Record) -> RetrieverResultItem:
    return RetrieverResultItem(content=f'{record.get("nodeText")}: score {record.get("score")}', metadata={"listIds": record.get("listIds")})

driver = create_driver

def create_retriever():
    return VectorCypherRetriever(
        driver,
        index_name=VECTOR_INDEX_NAME,
        retrieval_query=RETRIEVAL_QUERY,
        result_formatter=formatter,
        embedder=create_embedder,
        neo4j_database='neo4j',
    )