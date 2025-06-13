from notion_client import Client
import os
from dotenv import load_dotenv
import time
from typing import List, Tuple, Dict, Any

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))

def fetch_blocks(page_id: str) -> List[Dict[str, Any]]:
    """Fetch all blocks from a Notion page with error handling."""
    results = []
    cursor = None
    max_retries = 3
    
    while True:
        for attempt in range(max_retries):
            try:
                response = notion.blocks.children.list(
                    block_id=page_id, 
                    start_cursor=cursor,
                    page_size=100
                )
                results.extend(response['results'])
                
                if not response.get('has_more', False):
                    return results
                    
                cursor = response.get('next_cursor')
                break
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"⚠️  Failed to fetch blocks for page {page_id}: {e}")
                    return results
                else:
                    print(f"🔄 Retry {attempt + 1} for page {page_id}")
                    time.sleep(2 ** attempt)  # Exponential backoff
    
    return results

def extract_text_from_block(block: Dict[str, Any]) -> str:
    """Extract text from various Notion block types."""
    block_type = block.get("type")
    if not block_type:
        return ""
    
    text_parts = []
    
    # Handle different block types
    if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item"]:
        rich_text = block.get(block_type, {}).get("rich_text", [])
        for text_obj in rich_text:
            text_parts.append(text_obj.get("plain_text", ""))
    
    elif block_type == "code":
        code_text = block.get("code", {}).get("rich_text", [])
        for text_obj in code_text:
            text_parts.append(text_obj.get("plain_text", ""))
    
    elif block_type == "quote":
        quote_text = block.get("quote", {}).get("rich_text", [])
        for text_obj in quote_text:
            text_parts.append(f"> {text_obj.get('plain_text', '')}")
    
    elif block_type == "callout":
        callout_text = block.get("callout", {}).get("rich_text", [])
        for text_obj in callout_text:
            text_parts.append(text_obj.get("plain_text", ""))
    
    elif block_type == "toggle":
        toggle_text = block.get("toggle", {}).get("rich_text", [])
        for text_obj in toggle_text:
            text_parts.append(text_obj.get("plain_text", ""))
    
    return " ".join(text_parts)

def extract_text(blocks: List[Dict[str, Any]]) -> str:
    """Extract text from a list of Notion blocks."""
    texts = []
    for block in blocks:
        text = extract_text_from_block(block)
        if text.strip():
            texts.append(text.strip())
    return "\n\n".join(texts)

def fetch_database_pages(database_id: str) -> List[Dict[str, Any]]:
    """Fetch all pages from a Notion database with error handling."""
    pages = []
    cursor = None
    max_retries = 3
    
    print(f"📥 Fetching pages from database: {database_id}")
    
    while True:
        for attempt in range(max_retries):
            try:
                response = notion.databases.query(
                    database_id=database_id, 
                    start_cursor=cursor,
                    page_size=100
                )
                pages.extend(response["results"])
                
                if not response.get("has_more", False):
                    return pages
                    
                cursor = response.get("next_cursor")
                break
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ Failed to fetch database pages: {e}")
                    return pages
                else:
                    print(f"🔄 Retry {attempt + 1} for database query")
                    time.sleep(2 ** attempt)
    
    return pages

def extract_page_title(page: Dict[str, Any]) -> str:
    """Extract title from a Notion page."""
    properties = page.get("properties", {})
    
    # Look for title property
    for prop_name, prop_data in properties.items():
        if prop_data.get("type") == "title":
            title_array = prop_data.get("title", [])
            if title_array:
                return "".join([t.get("plain_text", "") for t in title_array])
    
    return "Untitled"

def fetch_all_texts_from_database(database_id: str) -> List[Tuple[str, str]]:
    """
    Fetch all text content from pages in a Notion database.
    Returns a list of (title, content_text) tuples.
    """
    if not database_id:
        raise ValueError("Database ID is required")
    
    pages = fetch_database_pages(database_id)
    if not pages:
        print("⚠️  No pages found in database")
        return []
    
    print(f"📄 Found {len(pages)} pages. Processing content...")
    all_texts = []

    for i, page in enumerate(pages, 1):
        page_id = page["id"]
        title = extract_page_title(page)
        
        print(f"🔄 Processing page {i}/{len(pages)}: {title}")
        
        try:
            blocks = fetch_blocks(page_id)
            text = extract_text(blocks)
            
            if text.strip():
                all_texts.append((title, text))
                print(f"   ✅ Extracted {len(text)} characters")
            else:
                print(f"   ⚠️  No content found")
                
        except Exception as e:
            print(f"   ❌ Error processing page: {e}")
            continue
        
        # Rate limiting
        time.sleep(0.3)

    print(f"\n✅ Successfully processed {len(all_texts)} pages with content")
    return all_texts


