import os
import traceback

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

print(
    "OPENAI_API_KEY EXISTS:",
    bool(os.getenv("OPENAI_API_KEY"))
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)


def generate_response(
    question,
    context
):

    print(
        "DEBUG: generate_response called"
    )

    return f"""
QUESTION:
{question}

CONTEXT:
{context}
"""