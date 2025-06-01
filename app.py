from indexing.embed import main as embed_main
from rag_agent.answer import generate_answer, retrieve_top_chunks
import os
import json
import numpy as np

def load_embeddings():
    with open("embeddings.json", "r") as f:
        data = json.load(f)
    for d in data:
        d["embedding"] = np.array(d["embedding"])
    return data

def main():
    print("1) Build embeddings from Notion (if not done)")
    print("2) Ask a question")
    choice = input("Choose: ")
    if choice == "1":
        embed_main()
        print("Done embedding")
    elif choice == "2":
        embeddings = load_embeddings()
        query = input("Enter your question: ")
        # embed query
        query_emb = embed_text(query)  # reuse embed_text from embed.py
        chunks = retrieve_top_chunks(query_emb, embeddings)
        answer = generate_answer(query, chunks)
        print("\nAnswer:\n", answer)

if __name__ == "__main__":
    main()
