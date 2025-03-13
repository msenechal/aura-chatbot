from neo4j import GraphDatabase
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from config import OPENAI_API_KEY, NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

api_key = OPENAI_API_KEY

embedder = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

with driver.session() as session:
    res = session.run(
        """
        MATCH (e:Chunk)
        WHERE e.text IS NOT NULL AND e.morganEmbedding IS NULL
        RETURN e.id as id, e.text as data
        """
    )
    for record in res:
        chunk_id = record["id"]
        data = record["data"]
        if len(data) > 12000:
            print(f"Skipping chunks {chunk_id} with data length {len(data)}")
            continue
        print(f"Embedding chunk {chunk_id}")
        embedding = embedder.embed_query(data)
        session.run(
            """
            MATCH (e:Chunk {id: $chunk_id})
            SET e.morganEmbedding = $embedding
            """,
            chunk_id=chunk_id,
            embedding=embedding
        )