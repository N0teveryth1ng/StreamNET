import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

client = chromadb.CloudClient(
    api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE")
)

collection = client.get_or_create_collection(
    name="division_memory"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def store_memory(id, text):
    embedding = model.encode(text).tolist()

    collection.add(
        ids=[id],
        documents=[text],
        embeddings=[embedding]
    )


def search_memory(query):
    embedding = model.encode(query).tolist()

    return collection.query(
        query_embeddings=[embedding],
        n_results=3
    )