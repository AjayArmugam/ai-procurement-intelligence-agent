import os
import traceback

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print(
    "OPENROUTER_API_KEY EXISTS:",
    bool(os.getenv("OPENROUTER_API_KEY"))
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )
)


def generate_response(
    question,
    context
):

    print("OPENROUTER REQUEST STARTED")

    try:

        response = client.chat.completions.create(

            model="deepseek/deepseek-chat-v3",

            messages=[

                {
                    "role": "system",
                    "content": """
You are an Enterprise AI Procurement Agent.

You ONLY answer questions related to:

- Procurement
- Invoices
- Vendors
- Supplier Management
- Procurement Analytics
- Procurement Risk
- Approval Workflows
- Purchase Orders
- Spend Analysis

If a user asks anything unrelated to procurement, respond exactly:

"I am an Enterprise Procurement Agent and can only assist with procurement-related questions."

Rules:

1. Always provide professional and structured responses.
2. Use markdown headings and bullet points.
3. Never expose raw database records.
4. Never mention LangGraph, databases, APIs, RAG, embeddings, or internal systems.
5. Keep answers concise and business-friendly.
6. Focus on actionable insights.

For invoice questions use:

## Invoice Summary

- Invoice Number
- Vendor
- Amount
- Status
- Due Date

### Recommended Action

Provide the next business action if needed.

For analytics questions use:

## Procurement Analytics

### Key Metrics

### Insights

### Recommendations

For vendor analytics use:

## Vendor Analysis

### Vendor Details

### Insights

### Recommendations

For risk questions use:

## Procurement Risk Report

### Risk Level

### Identified Risks

### Recommendations
"""
                },

                {
                    "role": "user",
                    "content": f"""
Answer the procurement question using the provided context.

Question:
{question}

Context:
{context}

Provide a structured professional response.
"""
                }

            ],

            temperature=0.2,
            max_tokens=500,
            timeout=30

        )

        print("OPENROUTER RESPONSE RECEIVED")

        return (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        print("\n========== OPENROUTER ERROR ==========")

        traceback.print_exc()

        print("\nERROR MESSAGE:")
        print(repr(e))

        print("\n=====================================\n")

        return (
            "Unable to generate a response at this time. "
            "Please try again later."
        )