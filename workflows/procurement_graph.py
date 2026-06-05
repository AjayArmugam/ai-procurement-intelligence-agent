from typing import TypedDict
import re

from database.postgres import (
    get_invoice_status,
    update_invoice_status,
    get_total_pending_amount,
    get_all_unpaid_invoices,
    get_total_approved_invoices,
    get_total_procurement_spend,
    get_top_vendor_by_spend,
    get_vendor_spend
)

from rag.retriever import (
    search_documents
)

from agents.response_agent import (
    generate_response
)
from agents.risk_agent import (
    risk_agent
)

from langgraph.graph import (
    StateGraph,
    END
)


# =====================================
# State
# =====================================

class ProcurementState(TypedDict):
    question: str
    intent: str
    context: str
    answer: str


# =====================================
# Intent Agent
# =====================================
def detect_intent(state):

    print("Entering Intent Agent")

    question = state["question"].lower()

    # Approval Actions

    if re.search(
        r"(approve|reject)\s+invoice",
        question
    ):

        state["intent"] = "approval"

    # Analytics Queries

    elif (
        "pending amount" in question
        or "unpaid invoices" in question
        or "approved invoice" in question
        or "approved invoices" in question
        or "how many approved" in question
        or "procurement spend" in question
        or "total spend" in question
    ):

        state["intent"] = "analytics"
    # Vendor Analytics

    elif (
        "highest spend" in question
        or "top vendor" in question
        or "vendor spend" in question
        or "spent with" in question
    ):
        
        state["intent"] = "vendor_analytics"

    elif (
        "risk" in question
        or "risks" in question
        or "procurement risk" in question
    ):
        state["intent"] = "risk"

    # Database Queries

    elif (
        "status" in question
    ):

        state["intent"] = "database"

    elif (
        "summary" in question
        or "business justification" in question
        or "line item" in question
        or "invoice details" in question
        or "invoice summary" in question
    ):
        state["intent"] = "rag"

    elif (
            "report" in question
            or "executive" in question
        ):
            state["intent"] = "summary"

    # RAG Queries

    else:

        state["intent"] = "rag"

    print(
        "Detected Intent:",
        state["intent"]
    )

    

    return state
# =====================================
# Database Agent
# =====================================

def database_agent(state):

    print("Entering Database Agent")

    question = state["question"]

    invoice_match = re.search(
        r"INV-\d+",
        question,
        re.IGNORECASE
    )

    if invoice_match:

        invoice_number = (
            invoice_match.group()
            .upper()
        )

        result = get_invoice_status(
            invoice_number
        )

        if result:

            state["context"] = str(result)

        else:

            state["context"] = (
                "Invoice not found."
            )

    else:

        state["context"] = (
            "No invoice number found."
        )

    return state


# =====================================
# Approval Agent
# =====================================

def approval_agent(state):

    print("Entering Approval Agent")

    question = state["question"]

    invoice_match = re.search(
        r"INV-\d+",
        question,
        re.IGNORECASE
    )

    if not invoice_match:

        state["context"] = (
            "No invoice number found."
        )

        return state

    invoice_number = (
        invoice_match.group()
        .upper()
    )

    if "approve" in question.lower():

        result = update_invoice_status(
            invoice_number,
            "APPROVED"
        )

    elif "reject" in question.lower():

        result = update_invoice_status(
            invoice_number,
            "REJECTED"
        )

    else:

        result = {
            "message":
            "Unknown action."
        }

    state["context"] = str(result)

    return state

# =====================================
# Analytics Agent
# =====================================

def analytics_agent(state):

    print("Entering Analytics Agent")

    question = state["question"].lower()

    if "pending amount" in question:

        result = get_total_pending_amount()

    elif "unpaid invoices" in question:

        result = get_all_unpaid_invoices()

    elif "approved" in question:

        result = get_total_approved_invoices()

    elif "procurement spend" in question:

        result = get_total_procurement_spend()

    else:

        result = {
            "message":
            "Analytics query not supported."
        }

    state["context"] = str(result)

    return state

# =====================================
# Vendor Analytics Agent
# =====================================

def vendor_analytics_agent(state):

    print(
        "Entering Vendor Analytics Agent"
    )

    question = state["question"]

    # Top Vendor Query

    if (
        "highest spend" in question.lower()
        or "top vendor" in question.lower()
    ):

        result = (
            get_top_vendor_by_spend()
        )

    # Specific Vendor Query

    else:

        vendor_names = [
            "MedSupply Inc"
        ]

        found_vendor = None

        for vendor in vendor_names:

            if vendor.lower() in question.lower():

                found_vendor = vendor

                break

        if found_vendor:

            result = (
                get_vendor_spend(
                    found_vendor
                )
            )

        else:

            result = {
                "message":
                "Vendor not found."
            }

    state["context"] = str(result)

    return state

# =====================================
# RAG Agent
# =====================================

def rag_agent(state):

    print("Entering RAG Agent")

    query = state["question"]

    results = search_documents(
        query
    )

    documents = results[
        "documents"
    ][0]

    metadata = results.get(
        "metadatas",
        [[]]
    )[0]

    context = "\n\n".join(
        documents
    )

    source_text = ""

    if metadata:

        invoices = set()

        for item in metadata:

            if (
                "invoice_number"
                in item
            ):

                invoices.add(
                    item["invoice_number"]
                )

        if invoices:

            source_text = "\n\nSources:\n"

            for invoice in invoices:

                source_text += (
                    f"• {invoice}\n"
                )

    state["context"] = (
        context
        + source_text
    )
    

    return state


# =====================================
# Response Agent
# =====================================

def response_agent(state):

    print("Entering Response Agent")

    answer = generate_response(
        state["question"],
        state["context"]
    )
    state["answer"] = answer

    return state


# =====================================
# Summary Agent
# =====================================

def summary_agent(state):

    print(
        "Entering Summary Agent"
    )

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

    unpaid = (
        get_all_unpaid_invoices()
    )

    context = f"""
Executive Procurement Summary

Total Procurement Spend:
{total_spend}

Pending Amount:
{pending_amount}

Approved Invoices:
{approved}

Top Vendor:
{top_vendor}

Unpaid Invoices:
{unpaid}
"""

    state["context"] = context

    return state

# =====================================
# Router
# =====================================

def route_intent(state):

    return state["intent"]


# =====================================
# Build Graph
# =====================================

graph = StateGraph(
    ProcurementState
)

# Nodes

graph.add_node(
    "intent_agent",
    detect_intent
)

graph.add_node(
    "database_agent",
    database_agent
)

graph.add_node(
    "approval_agent",
    approval_agent
)

graph.add_node(
    "analytics_agent",
    analytics_agent
)

graph.add_node(
    "vendor_analytics_agent",
    vendor_analytics_agent
)

graph.add_node(
    "rag_agent",
    rag_agent
)
graph.add_node(
    "summary_agent",
    summary_agent
)
graph.add_node(
    "risk_agent",
    risk_agent
)

graph.add_node(
    "response_agent",
    response_agent
)

# Entry Point

graph.set_entry_point(
    "intent_agent"
)

# Conditional Routing

graph.add_conditional_edges(
    "intent_agent",
    route_intent,
    {
        "database":
        "database_agent",

        "approval":
        "approval_agent",

        "analytics":
        "analytics_agent",

        "vendor_analytics":
        "vendor_analytics_agent",
        
        "summary":
        "summary_agent",

        "rag":
        "rag_agent",

        "risk":
        "risk_agent",


    }
)

# Database → Response

graph.add_edge(
    "database_agent",
    "response_agent"
)

# Approval → Response

graph.add_edge(
    "approval_agent",
    "response_agent"
)

graph.add_edge(
    "analytics_agent",
    "response_agent"
)

graph.add_edge(
    "vendor_analytics_agent",
    "response_agent"
)
graph.add_edge(
    "summary_agent",
    "response_agent"
)
graph.add_edge(
    "risk_agent",
    "response_agent"
)
# RAG → Response

graph.add_edge(
    "rag_agent",
    "response_agent"
)

# Response → END

graph.add_edge(
    "response_agent",
    END
)

# Compile

app = graph.compile()


# =====================================
# Test
# =====================================

if __name__ == "__main__":

    result = app.invoke(
        {
            "question":
            "Approve invoice INV-1002",

            "intent": "",

            "context": "",

            "answer": ""
        }
    )

    print("\nFINAL ANSWER:\n")

    print(
        result["answer"]
    )
