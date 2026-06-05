import chromadb
import re

from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="procurement_docs"
)

print(
    "COLLECTION COUNT:",
    collection.count()
)

model = None


def get_model():

    global model

    if model is None:

        print(
            "Loading Embedding Model..."
        )

        model = SentenceTransformer(
            "./models/all-MiniLM-L6-v2"
        )

    return model


def search_documents(
    query,
    n_results=3
):

    invoice_match = re.search(
        r"INV-\d+",
        query,
        re.IGNORECASE
    )

    if invoice_match:

        invoice_number = (
            invoice_match.group()
            .upper()
        )

        results = collection.get(
            where={
                "invoice_number":
                invoice_number
            }
        )

        matching_docs = (
            results["documents"]
        )

        if matching_docs:

            metadata = []

            for _ in matching_docs:

                metadata.append(
                    {
                        "invoice_number":
                        invoice_number
                    }
                )

            return {
                "documents": [
                    matching_docs
                ],
                "metadatas": [
                    metadata
                ]
            }

    model = get_model()

    query_embedding = (
        model.encode(query)
        .tolist()
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )

    return results