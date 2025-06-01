import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY is not set in .env")
    exit()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"  # Groq uses OpenAI-compatible API
)

def test_groq():
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "user", "content": "Hi! What's the capital of Germany?"}
            ],
            max_tokens=50
        )
        print("✅ Response from Groq:")
        print(response.choices[0].message.content)
    except Exception as e:
        print("❌ Error calling Groq API:", e)

if __name__ == "__main__":
    test_groq()
