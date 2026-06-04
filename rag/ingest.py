from pathlib import Path
import re

import chromadb

from pypdf import PdfReader

from sentence_transformers import SentenceTransformer

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

# =====================================
# ChromaDB Initialization
# =====================================

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="procurement_docs"
)

# =====================================
# Embedding Model
# =====================================

model = SentenceTransformer(
    "./models/all-MiniLM-L6-v2"
)

# =====================================
# PDF Text Extraction
# =====================================

def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


# =====================================
# Text Chunking
# =====================================

def chunk_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    return chunks


# =====================================
# Create Embeddings
# =====================================

def create_embedding(text):

    embedding = model.encode(text)

    return embedding


# =====================================
# Store Chunk in ChromaDB
# =====================================

def store_chunk(chunk, embedding, chunk_id, invoice_number):

    try:

        existing = collection.get(
            ids=[chunk_id]
        )

        if existing["ids"]:

            print(
                f"Skipping duplicate: {chunk_id}"
            )

            return

    except Exception:

        pass

    collection.add(
        ids=[chunk_id],
        documents=[chunk],
        embeddings=[embedding.tolist()],
        metadatas=[{"chunk_id": chunk_id, "invoice_number": invoice_number}]
    )

    print(
        f"Stored: {chunk_id}"
    )


# =====================================
# Ingest Single PDF
# =====================================

def ingest_pdf(pdf_path):

    text = extract_text(pdf_path)

    # Extract Invoice Number

    invoice_match = re.search(
        r"INV-\d+",
        text,
        re.IGNORECASE
    )

    if invoice_match:

        invoice_number = (
            invoice_match.group()
            .upper()
        )

    else:

        invoice_number = (
            Path(pdf_path)
            .stem
            .upper()
        )

    # Check if invoice already exists

    try:

        existing = collection.get(
            ids=[
                f"{invoice_number}_0"
            ]
        )

        if existing["ids"]:

            print(
                f"Invoice already exists: {invoice_number}"
            )

            return

    except Exception:

        pass

    chunks = chunk_text(text)

    for idx, chunk in enumerate(chunks):

        embedding = create_embedding(
            chunk
        )

        chunk_id = (
            f"{invoice_number}_{idx}"
        )

        store_chunk(
            chunk,
            embedding,
            chunk_id,
            invoice_number  
        )

    print(
        f"Ingested: {invoice_number}"
    )


# =====================================
# Ingest All PDFs
# =====================================

def ingest_all_pdfs():

    pdf_folder = Path("docs")

    pdf_files = list(
        pdf_folder.glob("*.pdf")
    )

    print(
        f"Found {len(pdf_files)} PDFs"
    )

    for pdf in pdf_files:

        ingest_pdf(
            str(pdf)
        )

    print(
        "\nAll PDFs Ingested Successfully!"
    )


# =====================================
# Search Documents
# =====================================

def search_documents(query, n_results=3):

    query_embedding = model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=n_results
    )

    return results


# =====================================
# Main
# =====================================

if __name__ == "__main__":

    ingest_all_pdfs()