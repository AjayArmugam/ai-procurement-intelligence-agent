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