# Integrating PINECONE momory

from pinecone import Pinecone
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv 



load_dotenv()

# call from .env
pinecone_api = os.getenv("PINECONE_API_KEY")



pc = Pinecone(api_key=pinecone_api)
index = pc.Index("division-memory")

model = SentenceTransformer("all-MiniLM-L6-v2")



# Store data
def store_data(id, text):
        embedding = model.encode(text).tolist()
    
        index.upsert([
            {
                "id": "doc1",
                "values": embedding,
                "metadata": {
                    "text": "CrewAI is a framework for multi-agent systems."
                }
            }
        ])



# search memory
def search_memory(query):
    
    embedding = model.encode(query).tolist()
    
    res = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True
    )
    
    return res


