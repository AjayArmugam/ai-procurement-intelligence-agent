# AI Procurement Intelligence Agent

An enterprise-grade AI Procurement Intelligence Agent built using LangGraph, FastAPI, PostgreSQL, ChromaDB, and Large Language Models.

The system automates procurement workflows by combining AI agents, Retrieval-Augmented Generation (RAG), procurement analytics, vendor analysis, approval workflows, and risk assessment into a single conversational interface.

---

## Features

### Procurement Analytics

* Total procurement spend analysis
* Pending payment tracking
* Approved invoice analytics
* Executive procurement summaries

### Vendor Intelligence

* Vendor spend analysis
* Top vendor identification
* Vendor concentration risk detection
* Procurement dependency analysis

### Invoice Intelligence (RAG)

* PDF invoice ingestion
* Semantic document search
* Invoice lookup using natural language
* Metadata-aware retrieval

### Procurement Risk Analysis

* Vendor concentration risk
* Outstanding payment risk
* Financial exposure analysis
* Actionable recommendations

### Approval Workflow

* Approve invoices using natural language
* Reject invoices using natural language
* Database-backed status updates
* Audit-friendly workflow execution

### Conversational AI

* Intent classification
* Multi-agent workflow orchestration
* DeepSeek/OpenRouter-powered responses
* Executive-style reporting

---

## Architecture

Frontend (React + Vite)

↓

FastAPI Backend

↓

LangGraph Workflow

├── Intent Agent
├── RAG Agent
├── Analytics Agent
├── Vendor Analytics Agent
├── Risk Agent
├── Approval Agent
├── Summary Agent
└── Response Agent

↓

Data Layer

├── PostgreSQL
├── ChromaDB
└── PDF Knowledge Base

---

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS
* Axios
* Recharts

### Backend

* FastAPI
* LangGraph
* SQLAlchemy

### AI & RAG

* DeepSeek
* OpenRouter
* Sentence Transformers
* ChromaDB

### Database

* PostgreSQL

### Deployment

* Docker
* Docker Compose

---

## Project Structure

```text
agents/
api/
database/
docs/
frontend/
models/
rag/
scripts/
uploads/
workflows/

Dockerfile
docker-compose.yml
requirements.txt
```

---

## Example Queries

* What is invoice INV-2001?
* Show unpaid invoices.
* Generate a procurement summary.
* Which vendor has the highest spend?
* Approve invoice INV-1002.
* Reject invoice INV-1003.
* Generate a procurement risk report.

---

## Running Locally

### Backend

```bash
pip install -r requirements.txt
uvicorn api.app:api --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Docker Deployment

```bash
docker compose build
docker compose up
```

Backend:
http://localhost:8000

Frontend:
http://localhost:5173

---

## Future Improvements

* Multi-user authentication
* Role-based access control
* Procurement forecasting
* Contract intelligence
* Supplier performance scoring
* Real-time approval notifications

---

## Author

Ajay Armugam
