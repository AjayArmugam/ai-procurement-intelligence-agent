import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="procurement_docs"
)

collection.delete(
    ids=[
        "invoice-9999_0",
        "invoice-9999_1"
    ]
)

print("Deleted duplicate chunks")