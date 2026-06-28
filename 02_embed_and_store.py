from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

# ---- Step 1: PDF load karo (pichla code reuse) ----
def load_pdf(filepath):
    reader = PdfReader(filepath)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

def split_into_chunks(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "]
    )
    return splitter.split_text(text)

# ---- Step 2: Embedding model load karo ----
# Ye model free hai, local chalta hai, koi API call nahi hoti
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---- Step 3: Qdrant client banao (local, in-memory abhi ke liye) ----
qdrant = QdrantClient(path="local_qdrant_db")  # local folder mein save hoga

COLLECTION_NAME = "hr_handbook"

# ---- Step 4: Collection banao (jaise ek table database mein) ----
qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    # size=384 kyunki all-MiniLM-L6-v2 model 384-dimension vectors banata hai
)

# ---- Step 5: PDF process karo ----
print("Loading and chunking PDF...")
text = load_pdf("documents/company_handbook.pdf")
chunks = split_into_chunks(text)
print(f"Created {len(chunks)} chunks")

# ---- Step 6: Har chunk ka embedding banao aur Qdrant mein store karo ----
print("Generating embeddings and storing in Qdrant...")
points = []
for chunk in chunks:
    vector = embedding_model.encode(chunk).tolist()
    point = PointStruct(
        id=str(uuid.uuid4()),       # har chunk ka unique ID
        vector=vector,                # uska embedding
        payload={"text": chunk}       # original text bhi save karo, taake retrieve kar sakein
    )
    points.append(point)

qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

print(f"Successfully stored {len(points)} chunks in Qdrant!")
print("\nDone. Vector database is ready for retrieval.")