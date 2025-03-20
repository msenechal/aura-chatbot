from embedding import Embedding
from driver import Neo4jDriver


embedder = Embedding.get_instance().embedder
driver = Neo4jDriver.get_instance().driver

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