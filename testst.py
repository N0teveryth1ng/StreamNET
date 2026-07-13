import time

print("Importing...")

from sentence_transformers import SentenceTransformer

print("Imported")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loaded")