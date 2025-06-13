import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def test_openai_api():
    try:
        print("🔑 API key starts with:", api_key[:8])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello! What's the capital of France?"}],
            max_tokens=50
        )
        print("\n✅ Response:", response.choices[0].message.content)
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    test_openai_api()
