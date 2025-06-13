#!/usr/bin/env python3
"""
Notion AI Assistant - Main Application

This is the entry point for the AI agent that retrieves and processes data from Notion databases.
"""

import os
import sys
from typing import List, Dict
from dotenv import load_dotenv

# Import our custom modules
from indexing.embed import main as embed_main, load_embeddings as load_embed_file
from rag_agent.answer import generate_answer, retrieve_top_chunks, embed_query, load_embeddings

load_dotenv()

def print_banner():
    """Print application banner."""
    print("=" * 60)
    print("🤖 NOTION AI ASSISTANT")
    print("=" * 60)
    print("Your intelligent agent for Notion database queries")
    print()

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ["NOTION_API_KEY", "NOTION_DATABASE_ID", "OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease add them to your .env file")
        return False
    
    print("✅ Environment variables configured")
    return True

def interactive_mode():
    """Run the assistant in interactive mode."""
    print("\n🔄 Loading embeddings...")
    embeddings = load_embeddings()
    
    if not embeddings:
        print("\n❌ No embeddings found. Please run option 1 first to index your Notion database.")
        return
    
    print(f"✅ Loaded {len(embeddings)} embeddings")
    print("\n💬 Interactive mode started. Type 'quit' to exit.")
    print("   Example questions:")
    print("   - What is our standard for writing unit tests?")
    print("   - What's the deployment procedure?")
    print("   - Are there any best practices for API error handling?")
    print()
    
    while True:
        try:
            query = input("🤔 Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if not query:
                continue
            
            print("\n🔍 Searching for relevant information...")
            
            # Embed the query
            query_embedding = embed_query(query)
            if not query_embedding:
                print("❌ Failed to process your question. Please try again.")
                continue
            
            # Retrieve relevant chunks
            relevant_chunks = retrieve_top_chunks(query_embedding, embeddings, top_k=5)
            
            if not relevant_chunks:
                print("❌ No relevant information found. Try rephrasing your question.")
                continue
            
            print("💡 Generating answer...")
            answer = generate_answer(query, relevant_chunks)
            
            print("\n" + "="*50)
            print("📝 ANSWER:")
            print("="*50)
            print(answer)
            print("\n" + "="*50)
            
            # Show sources
            print("\n📚 SOURCES:")
            for i, chunk in enumerate(relevant_chunks[:3], 1):
                title = chunk.get("title", "Unknown")
                print(f"  {i}. {title}")
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")

def show_stats():
    """Show statistics about the indexed data."""
    embeddings = load_embeddings()
    if not embeddings:
        print("❌ No embeddings found. Run indexing first.")
        return
    
    titles = set()
    total_chunks = len(embeddings)
    
    for emb in embeddings:
        titles.add(emb.get("title", "Unknown"))
    
    print(f"\n📊 STATISTICS:")
    print(f"   📄 Total pages indexed: {len(titles)}")
    print(f"   📝 Total chunks: {total_chunks}")
    print(f"   📚 Average chunks per page: {total_chunks / len(titles):.1f}")
    print()
    
    print("📋 Indexed pages:")
    for title in sorted(titles):
        count = sum(1 for emb in embeddings if emb.get("title") == title)
        print(f"   - {title} ({count} chunks)")

def main():
    """Main application entry point."""
    print_banner()
    
    if not check_environment():
        sys.exit(1)
    
    while True:
        print("\n🔧 MAIN MENU:")
        print("1. 🔄 Index Notion Database (Create/Update embeddings)")
        print("2. 💬 Ask Questions (Interactive mode)")
        print("3. 📊 Show Statistics")
        print("4. 🧪 Test Single Question")
        print("5. 🚪 Exit")
        
        try:
            choice = input("\nChoose an option (1-5): ").strip()
            
            if choice == "1":
                print("\n🔄 Starting indexing process...")
                embed_main()
                print("\n✅ Indexing completed!")
                
            elif choice == "2":
                interactive_mode()
                
            elif choice == "3":
                show_stats()
                
            elif choice == "4":
                embeddings = load_embeddings()
                if not embeddings:
                    print("❌ No embeddings found. Run indexing first.")
                    continue
                
                query = input("\n🤔 Enter your question: ").strip()
                if query:
                    print("🔍 Processing...")
                    query_embedding = embed_query(query)
                    if query_embedding:
                        relevant_chunks = retrieve_top_chunks(query_embedding, embeddings, top_k=3)
                        answer = generate_answer(query, relevant_chunks)
                        print(f"\n📝 Answer: {answer}")
                
            elif choice == "5":
                print("\n👋 Thank you for using Notion AI Assistant!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
