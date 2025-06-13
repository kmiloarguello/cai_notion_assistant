#!/usr/bin/env python3
"""
LLM providers - Support for multiple language model services
"""

import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_answer(self, query: str, context_chunks: List[Dict], **kwargs) -> str:
        """Generate an answer using the retrieved context chunks."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the LLM provider."""
        pass

class OpenAILLMProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not available. Install with: pip install openai")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self._name = f"OpenAI-{model}"
    
    def generate_answer(self, query: str, context_chunks: List[Dict], **kwargs) -> str:
        """Generate an answer using OpenAI models."""
        if not context_chunks:
            return "I couldn't find relevant information to answer your question. Please try rephrasing or check if the data has been indexed."
        
        # Prepare context with source information
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            title = chunk.get("title", "Unknown")
            content = chunk.get("chunk", "")
            context_parts.append(f"Source {i} - {title}:\n{content}")
        
        context_text = "\n\n---\n\n".join(context_parts)
        
        prompt = f"""You are an AI assistant helping with questions about our team's documentation and knowledge base. 
Answer the user's question based on the following context from our Notion database.

If the context doesn't contain enough information to answer the question completely, say so and suggest what additional information might be needed.

Context:
{context_text}

Question: {query}

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating answer with OpenAI: {e}"
    
    @property
    def name(self) -> str:
        return self._name

class GroqLLMProvider(LLMProvider):
    """Groq LLM provider."""
    
    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package required for Groq compatibility. Install with: pip install openai")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = model
        self._name = f"Groq-{model}"
    
    def generate_answer(self, query: str, context_chunks: List[Dict], **kwargs) -> str:
        """Generate an answer using Groq models."""
        if not context_chunks:
            return "I couldn't find relevant information to answer your question. Please try rephrasing or check if the data has been indexed."
        
        # Prepare context with source information
        context_parts = []
        for i, chunk in enumerate(context_chunks, 1):
            title = chunk.get("title", "Unknown")
            content = chunk.get("chunk", "")
            context_parts.append(f"Source {i} - {title}:\n{content}")
        
        context_text = "\n\n---\n\n".join(context_parts)
        
        prompt = f"""You are an AI assistant helping with questions about our team's documentation and knowledge base. 
Answer the user's question based on the following context from our Notion database.

If the context doesn't contain enough information to answer the question completely, say so and suggest what additional information might be needed.

Context:
{context_text}

Question: {query}

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 1000)
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating answer with Groq: {e}"
    
    @property
    def name(self) -> str:
        return self._name

def get_llm_provider(provider_type: str = "auto") -> Optional[LLMProvider]:
    """Get the best available LLM provider."""
    
    if provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OpenAI API key not found")
            return None
        try:
            return OpenAILLMProvider(api_key)
        except Exception as e:
            print(f"❌ Failed to initialize OpenAI LLM provider: {e}")
            return None
    
    elif provider_type == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("❌ Groq API key not found")
            return None
        try:
            return GroqLLMProvider(api_key)
        except Exception as e:
            print(f"❌ Failed to initialize Groq LLM provider: {e}")
            return None
    
    elif provider_type == "auto":
        # Try OpenAI first, then Groq
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and OPENAI_AVAILABLE:
            try:
                provider = OpenAILLMProvider(openai_key)
                print("✅ Using OpenAI for LLM")
                return provider
            except Exception as e:
                print(f"⚠️  OpenAI LLM not available: {e}")
        
        # Try Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and OPENAI_AVAILABLE:
            try:
                provider = GroqLLMProvider(groq_key)
                print("✅ Using Groq for LLM")
                return provider
            except Exception as e:
                print(f"❌ Groq LLM failed: {e}")
        
        print("❌ No LLM providers available")
    
    return None

def list_available_llm_providers() -> List[str]:
    """List all available LLM providers."""
    providers = []
    
    if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
        providers.append("openai")
    
    if OPENAI_AVAILABLE and os.getenv("GROQ_API_KEY"):
        providers.append("groq")
    
    return providers
