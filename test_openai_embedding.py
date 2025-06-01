import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY is not set in the .env file.")
    exit()

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def test_embedding():
    try:
        # Text to be embedded
        text = "Paris is the capital of France."

        # Create embedding
        response = client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )

        # Extract and print the embedding
        embedding = response.data[0].embedding
        print("✅ Successfully generated embedding.")
        print(f"Embedding length: {len(embedding)}")
        print(f"First 5 dimensions: {embedding[:5]}")
    except Exception as e:
        print("❌ Error generating embedding:", e)

if __name__ == "__main__":
    test_embedding()
