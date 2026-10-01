
import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


# Project paths
BASE_DIR = Path(__file__).resolve().parent
POLICY_DIR = BASE_DIR / "company_policies"
INDEX_PATH = BASE_DIR / "policy_index.faiss"
METADATA_PATH = BASE_DIR / "policy_metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_policy_chunks():
    """Read policy files and split them into paragraph-based chunks."""

    chunks = []
    source_names = []

    policy_files = sorted(POLICY_DIR.glob("*.txt"))

    if not policy_files:
        raise FileNotFoundError(
            f"No .txt policy files found in {POLICY_DIR}"
        )

    for path in policy_files:
        text = path.read_text(encoding="utf-8")

        # Split at blank lines, keeping each paragraph together.
        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        for paragraph in paragraphs:
            chunks.append(paragraph)
            source_names.append(path.name)

    return chunks, source_names


def build_policy_index():
    """Create embeddings and save the FAISS index and metadata."""

    print("Loading policy documents...")
    chunks, source_names = load_policy_chunks()

    print(f"Loaded {len(chunks)} policy chunks.")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    ).astype("float32")

    print("Building FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    print("Saving index and metadata...")
    faiss.write_index(index, str(INDEX_PATH))

    metadata = {
        "model_name": MODEL_NAME,
        "chunks": chunks,
        "source_names": source_names,
    }

    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Index saved to: {INDEX_PATH.name}")
    print(f"Metadata saved to: {METADATA_PATH.name}")
    print("Policy ingestion completed successfully!")


if __name__ == "__main__":
    build_policy_index()
