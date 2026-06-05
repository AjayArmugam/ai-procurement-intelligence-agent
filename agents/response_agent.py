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
                    "content":
                    "You are a procurement assistant."
                },
                {
                    "role": "user",
                    "content":
                    f"""
Question:
{question}

Context:
{context}
"""
                }
            ],

            temperature=0.3,
            max_tokens=300,
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

        return f"ERROR: {str(e)}"