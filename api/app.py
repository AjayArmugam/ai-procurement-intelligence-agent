from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil

from workflows.procurement_graph import (
    app as procurement_graph
)

from rag.ingest import ingest_pdf

from database.postgres import (
    get_invoice_status,
    get_total_procurement_spend,
    get_total_pending_amount,
    get_total_approved_invoices,
    get_top_vendor_by_spend
)

# =====================================
# Request Models
# =====================================

class QueryRequest(BaseModel):
    question: str


# =====================================
# FastAPI App
# =====================================

api = FastAPI(
    title="AI Procurement Agent",
    version="1.0.0",
    description="Enterprise AI Procurement & Invoice Intelligence Agent"
)

# =====================================
# CORS CONFIGURATION
# =====================================

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-procurement-intelligence-agent.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# Root Endpoint
# =====================================

@api.get("/")
def root():

    return {
        "message":
        "AI Procurement Agent Running"
    }


# =====================================
# Health Check
# =====================================

@api.get("/health")
def health():

    return {
        "status": "healthy"
    }


# =====================================
# Query Endpoint
# =====================================

@api.post("/query")
def query_agent(request: QueryRequest):

    try:

        result = procurement_graph.invoke(
            {
                "question": request.question,
                "intent": "",
                "context": "",
                "answer": ""
            }
        )

        return {
            "question": request.question,
            "answer": result["answer"]
        }

    except Exception as e:

        print("\nERROR IN QUERY ENDPOINT:")
        print(e)

        return {
            "error": str(e)
        }


# =====================================
# Upload PDF Endpoint
# =====================================

@api.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    upload_dir = "docs"

    os.makedirs(
        upload_dir,
        exist_ok=True
    )

    file_path = os.path.join(
        upload_dir,
        file.filename
    )

    if os.path.exists(file_path):

        return {
            "message":
            f"{file.filename} already exists"
        }

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    ingest_pdf(file_path)

    return {
        "message":
        f"{file.filename} uploaded successfully",

        "file_path":
        file_path
    }


# =====================================
# Invoice Endpoint
# =====================================

@api.get("/invoice/{invoice_number}")
def get_invoice(invoice_number: str):

    result = get_invoice_status(
        invoice_number.upper()
    )

    if result is None:

        return {
            "error":
            f"Invoice {invoice_number} not found"
        }

    return result


# =====================================
# Dashboard Endpoint
# =====================================

@api.get("/dashboard")
def dashboard():

    total_spend = (
        get_total_procurement_spend()
    )

    pending_amount = (
        get_total_pending_amount()
    )

    approved = (
        get_total_approved_invoices()
    )

    top_vendor = (
        get_top_vendor_by_spend()
    )

    return {

        "total_spend":
        float(
            total_spend["total_spend"]
        ),

        "pending_amount":
        float(
            pending_amount["total_pending"]
        ),

        "approved_invoices":
        approved["total_approved"],

        "top_vendor":
        top_vendor["vendor_name"]
    }