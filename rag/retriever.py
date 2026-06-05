import chromadb
import re
import os

print("CURRENT DIRECTORY:")
print(os.getcwd())

print("CHROMA EXISTS:")
print(os.path.exists("./chroma_db"))

if os.path.exists("./chroma_db"):
    print("CHROMA FILES:")
    print(os.listdir("./chroma_db"))

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