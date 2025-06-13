from embedding_providers import get_embedding_provider
from llm_providers import get_llm_provider
import numpy as np
import json
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    return np.dot(vec1_np, vec2_np) / (np.linalg.norm(vec1_np) * np.linalg.norm(vec2_np))

def retrieve_top_chunks(query_embedding: List[float], embeddings: List[Dict], top_k: int = 3) -> List[Dict]:
    """Retrieve the most relevant chunks based on cosine similarity."""
    if not embeddings:
        return []
    
    scores = []
    for embedding_data in embeddings:
        similarity = cosine_similarity(query_embedding, embedding_data["embedding"])
        scores.append((similarity, embedding_data))
    
    scores.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scores[:top_k]]

def embed_query(query: str) -> List[float]:
    """Generate embedding for the user query using available provider."""
    try:
        embedding_provider = get_embedding_provider("auto")
        if not embedding_provider:
            print("❌ No embedding provider available")
            return []
        
        return embedding_provider.embed_text(query)
    except Exception as e:
        print(f"Error embedding query: {e}")
        return []

def generate_answer(query: str, context_chunks: List[Dict], model_preference: str = "auto") -> str:
    """Generate an answer using the available LLM provider with fallback."""
    # Try OpenAI first
    if model_preference in ["auto", "openai"]:
        try:
            openai_provider = get_llm_provider("openai")
            if openai_provider:
                result = openai_provider.generate_answer(query, context_chunks)
                if not result.startswith("Error generating answer with OpenAI"):
                    return result
                else:
                    print("⚠️  OpenAI failed, trying Groq...")
        except Exception as e:
            print(f"⚠️  OpenAI error: {e}, trying Groq...")
    
    # Fall back to Groq if OpenAI fails or not preferred
    try:
        groq_provider = get_llm_provider("groq")
        if groq_provider:
            print("✅ Using Groq for answer generation")
            return groq_provider.generate_answer(query, context_chunks)
    except Exception as e:
        print(f"❌ Groq also failed: {e}")
    
    return "❌ No LLM provider available or all providers failed. Please check your API keys and quotas."

def load_embeddings(filename: str = "embeddings.json") -> List[Dict]:
    """Load embeddings from JSON file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Convert embedding lists back to numpy arrays for faster computation
        for item in data:
            if isinstance(item["embedding"], list):
                item["embedding"] = item["embedding"]  # Keep as list for JSON compatibility
        
        return data
    except FileNotFoundError:
        print(f"❌ Embeddings file not found: {filename}")
        print("Run the indexing process first with option 1 in the main menu.")
        return []
    except Exception as e:
        print(f"❌ Error loading embeddings: {e}")
        return []
