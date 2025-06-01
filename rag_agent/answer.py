from openai import OpenAI
import numpy as np

openai = OpenAI()

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def retrieve_top_chunks(query_embedding, embeddings, top_k=3):
    scores = [(cosine_similarity(query_embedding, e["embedding"]), e) for e in embeddings]
    scores.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scores[:top_k]]

def generate_answer(query, context_chunks):
    context_text = "\n\n".join([c["chunk"] for c in context_chunks])
    prompt = f"Answer the question based on the following context:\n\n{context_text}\n\nQuestion: {query}\nAnswer:"
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Later, you'll load saved embeddings from disk or vector DB
