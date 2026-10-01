import os
import faiss
from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Folder containing our company policies
policy_folder = "company_policies"

documents = []
document_names = []

# Read every .txt policy
for filename in os.listdir(policy_folder):
    if filename.endswith(".txt"):
        file_path = os.path.join(policy_folder, filename)

        with open(file_path, "r") as file:
            content = file.read()

        documents.append(content)
        document_names.append(filename)

# Convert policies into embeddings
embeddings = model.encode(documents)

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Ask the user a question
query = input("What would you like to know? ")

# Convert the question into an embedding
query_embedding = model.encode([query])

# Search for the most relevant policy
distances, results = index.search(query_embedding, k=1)

# Get the result
result_index = results[0][0]

context = documents[result_index]

print("\nRetrieved policy:")
print(document_names[result_index])

print("\nContext for the AI:")
print(context)

print("\nUser question:")
print(query)