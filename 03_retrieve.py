from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Same embedding model jo storage ke waqt use kiya tha
# IMPORTANT: hamesha same model use karna chahiye storage aur retrieval dono mein
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Same Qdrant database se connect karo
qdrant = QdrantClient(path="local_qdrant_db")
COLLECTION_NAME = "hr_handbook"

def retrieve_relevant_chunks(query, top_k=3):
    # User ke sawal ka embedding banao
    query_vector = embedding_model.encode(query).tolist()

    # Qdrant mein sabse close matching chunks dhoondo
    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    ).points

    return results

if __name__ == "__main__":
    query = "How many days of annual leave do I get?"

    print(f"Query: {query}\n")
    results = retrieve_relevant_chunks(query)

    for i, result in enumerate(results):
        print(f"--- Match {i+1} (score: {result.score:.4f}) ---")
        print(result.payload["text"])
        print()