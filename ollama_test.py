import requests
import os
import faiss
from sentence_transformers import SentenceTransformer

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Read company policies
documents = []
file_names = []

policy_folder = "company_policies"

for filename in os.listdir(policy_folder):
    if filename.endswith(".txt"):
        path = os.path.join(policy_folder, filename)

        with open(path, "r") as file:
            documents.append(file.read())

        file_names.append(filename)

# Create embeddings
document_embeddings = embedding_model.encode(documents)

# Create FAISS index
dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(document_embeddings)

# User question
question = "Can I work from home on Friday?"

# Embed the question
question_embedding = embedding_model.encode([question])

# Search FAISS
distance, indices = index.search(question_embedding, k=1)

# Get the most relevant document
result_index = indices[0][0]
context = documents[result_index]

print("Retrieved policy:", file_names[result_index])

# Send retrieved context to Llama
prompt = f"""
You are a workplace assistant.

Answer the user's question using ONLY the retrieved company policy.

Retrieved company policy:
{context}

User question:
{question}

If the policy does not provide enough information to answer something,
say that the information is not specified in the policy.

Answer clearly and briefly.
"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }
)

print("\nAnswer:")
print(response.json()["response"])