import time

start = time.time()

print("Importing...")

from sentence_transformers import SentenceTransformer

print("Imported in", time.time() - start, "seconds")

start = time.time()

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loaded in", time.time() - start, "seconds")

print(len(model.encode("hello")))