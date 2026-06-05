import chromadb
import re

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
# Search Documents
# =====================================

def search_documents(
    query,
    n_results=3
):

    print(
        "RAG TEMPORARILY DISABLED"
    )

    return {
        "documents": [
            [
                "No document context available."
            ]
        ],
        "metadatas": [
            []
        ]
    }