from notion_client.fetch import fetch_all_texts_from_database
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai = OpenAI()

def chunk_text(text, max_length=1000):
    # Simple splitter, can be improved (sentence split, etc)
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def embed_text(text):
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def main():
    database_id = os.getenv("NOTION_DATABASE_ID")
    pages = fetch_all_texts_from_database(database_id)

    embeddings = []
    for title, content in pages:
        chunks = chunk_text(content)
        for chunk in chunks:
            emb = embed_text(chunk)
            embeddings.append({
                "title": title,
                "chunk": chunk,
                "embedding": emb
            })

    # TODO: Save embeddings locally or to a vector DB
    print(f"Embedded {len(embeddings)} chunks")

if __name__ == "__main__":
    main()
