#!/usr/bin/env python3
"""
Embedding providers - Support for multiple embedding services
"""

import os
import time
from typing import List, Optional
from abc import ABC, abstractmethod
import numpy as np

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""
    
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for the given text."""
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the embedding provider."""
        pass

class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider."""
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not available. Install with: pip install openai")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self._name = f"OpenAI-{model}"
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            time.sleep(0.1)  # Rate limiting
            return response.data[0].embedding
        except Exception as e:
            print(f"Error with OpenAI embedding: {e}")
            return []
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts."""
        embeddings = []
        for text in texts:
            embedding = self.embed_text(text)
            if embedding:
                embeddings.append(embedding)
            else:
                embeddings.append([0.0] * 1536)  # Default dimension for text-embedding-3-small
        return embeddings
    
    @property
    def name(self) -> str:
        return self._name

class LocalEmbeddingProvider(EmbeddingProvider):
    """Local embedding provider using sentence-transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers package not available. Install with: pip install sentence-transformers")
        
        print(f"📥 Loading local embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        print("✅ Local embedding model loaded")
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        try:
            embedding = self.model.encode(text)
            return embedding.tolist()
        except Exception as e:
            print(f"Error with local embedding: {e}")
            return []
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts."""
        try:
            embeddings = self.model.encode(texts)
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            print(f"Error with local batch embedding: {e}")
            return []
    
    @property
    def name(self) -> str:
        return f"Local-{self.model_name}"

def get_embedding_provider(provider_type: str = "auto") -> Optional[EmbeddingProvider]:
    """Get the best available embedding provider."""
    
    if provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OpenAI API key not found")
            return None
        try:
            return OpenAIEmbeddingProvider(api_key)
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI provider: {e}")
            return None
    
    elif provider_type == "local":
        try:
            return LocalEmbeddingProvider()
        except Exception as e:
            print(f"❌ Failed to initialize local provider: {e}")
            return None
    
    elif provider_type == "auto":
        # Try OpenAI first, then fall back to local
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and OPENAI_AVAILABLE:
            try:
                provider = OpenAIEmbeddingProvider(api_key)
                # Test with a small text
                test_embedding = provider.embed_text("test")
                if test_embedding:
                    print("✅ Using OpenAI embeddings")
                    return provider
            except Exception as e:
                print(f"⚠️  OpenAI not available: {e}")
        
        # Fall back to local
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                print("📦 OpenAI not available, using local embeddings")
                return LocalEmbeddingProvider()
            except Exception as e:
                print(f"❌ Local embeddings failed: {e}")
        else:
            print("❌ No embedding providers available")
            print("Install sentence-transformers for local embeddings: pip install sentence-transformers")
    
    return None

def list_available_providers() -> List[str]:
    """List all available embedding providers."""
    providers = []
    
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
    
    if SENTENCE_TRANSFORMERS_AVAILABLE:
        providers.append("local")
    
    return providers
