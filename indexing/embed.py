from notion_fetcher.fetch import fetch_all_texts_from_database
from embedding_providers import get_embedding_provider, list_available_providers
import os
from dotenv import load_dotenv
import json
import time
from typing import List, Tuple

load_dotenv()

def chunk_text(text: str, max_length: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into chunks with overlap for better context preservation."""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_length
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Try to find a sentence boundary within the last 100 characters
        boundary_search = text[end-100:end]
        sentence_end = max(boundary_search.rfind('.'), boundary_search.rfind('!'), boundary_search.rfind('?'))
        
        if sentence_end > 0:
            end = end - 100 + sentence_end + 1
        
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks

def embed_text(text: str, provider=None) -> List[float]:
    """Generate embedding for text using the specified provider."""
    if provider is None:
        return []
    
    try:
        return provider.embed_text(text)
    except Exception as e:
        print(f"Error embedding text: {e}")
        return []

def save_embeddings(embeddings: List[dict], filename: str = "embeddings.json"):
    """Save embeddings to JSON file."""
    with open(filename, 'w') as f:
        json.dump(embeddings, f)
    print(f"Saved {len(embeddings)} embeddings to {filename}")

def load_embeddings(filename: str = "embeddings.json") -> List[dict]:
    """Load embeddings from JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No embeddings file found at {filename}")
        return []

def main():
    """Main function to process Notion database and create embeddings."""
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not database_id:
        print("❌ NOTION_DATABASE_ID not found in .env file")
        return
    
    # Get embedding provider
    print("🔍 Initializing embedding provider...")
    available_providers = list_available_providers()
    print(f"📋 Available providers: {available_providers}")
    
    if not available_providers:
        print("❌ No embedding providers available!")
        print("Install dependencies:")
        print("  For OpenAI: Set OPENAI_API_KEY in .env")
        print("  For local: pip install sentence-transformers torch")
        return
    
    # Choose provider
    if len(available_providers) == 1:
        provider_choice = available_providers[0]
    else:
        print("\n🔧 Multiple providers available:")
        for i, provider in enumerate(available_providers, 1):
            print(f"  {i}. {provider}")
        
        while True:
            try:
                choice = input(f"\nChoose provider (1-{len(available_providers)}) or press Enter for auto: ").strip()
                if not choice:
                    provider_choice = "auto"
                    break
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(available_providers):
                    provider_choice = available_providers[choice_idx]
                    break
                else:
                    print("❌ Invalid choice")
            except ValueError:
                print("❌ Please enter a number")
    
    embedding_provider = get_embedding_provider(provider_choice)
    if not embedding_provider:
        print("❌ Failed to initialize embedding provider")
        return
    
    print(f"✅ Using embedding provider: {embedding_provider.name}")
    
    print("🔍 Fetching pages from Notion database...")
    try:
        pages = fetch_all_texts_from_database(database_id)
        print(f"📄 Found {len(pages)} pages")
    except Exception as e:
        print(f"❌ Error fetching from Notion: {e}")
        return

    embeddings = []
    total_chunks = 0
    
    for i, (title, content) in enumerate(pages, 1):
        print(f"🔄 Processing page {i}/{len(pages)}: {title}")
        
        if not content.strip():
            print(f"⚠️  Skipping empty page: {title}")
            continue
            
        chunks = chunk_text(content)
        total_chunks += len(chunks)
        
        for j, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Skip very short chunks
                continue
                
            print(f"  📝 Embedding chunk {j+1}/{len(chunks)}")
            embedding = embed_text(chunk, embedding_provider)
            
            if embedding:  # Only add if embedding was successful
                embeddings.append({
                    "title": title,
                    "chunk": chunk,
                    "embedding": embedding,
                    "chunk_index": j,
                    "source": "notion_database",
                    "provider": embedding_provider.name
                })
    
    print(f"\n✅ Created {len(embeddings)} embeddings from {total_chunks} chunks")
    
    if embeddings:
        save_embeddings(embeddings)
        print("💾 Embeddings saved successfully!")
    else:
        print("❌ No embeddings were created")

if __name__ == "__main__":
    main()
