import chromadb
import re
import os

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

# =====================================
# Lazy Load Model
# =====================================

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


# =====================================
# Search Documents
# =====================================

def search_documents(
    query,
    n_results=3
):

    # =====================================
    # Exact Invoice Search
    # =====================================

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

        print(
            f"Looking for invoice: {invoice_number}"
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

            print(
                f"Exact Match Found: {invoice_number}"
            )

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

    # =====================================
    # Semantic Search
    # =====================================

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


    for doc in results[
        "documents"
    ][0]:

        print("=" * 50)
        print(doc)
        print()

    print("\n" + "=" * 50)
    print("QUERY:")
    print(query)


    print("=" * 50 + "\n")

    return results