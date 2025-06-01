from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))

def fetch_blocks(page_id):
    results = []
    cursor = None
    while True:
        response = notion.blocks.children.list(block_id=page_id, start_cursor=cursor)
        results.extend(response['results'])
        if not response['has_more']:
            break
        cursor = response['next_cursor']
    return results

def extract_text(blocks):
    texts = []
    for block in blocks:
        block_type = block.get("type")
        if block_type and "text" in block[block_type]:
            for t in block[block_type]["text"]:
                texts.append(t["plain_text"])
    return "\n".join(texts)

def fetch_database_pages(database_id):
    """Returns list of page objects inside a Notion database."""
    pages = []
    cursor = None
    while True:
        response = notion.databases.query(database_id=database_id, start_cursor=cursor)
        pages.extend(response["results"])
        if not response.get("has_more"):
            break
        cursor = response["next_cursor"]
    return pages

def fetch_all_texts_from_database(database_id):
    """Returns a list of (title, content_text) tuples from each page in the database."""
    from time import sleep
    pages = fetch_database_pages(database_id)
    all_texts = []

    for page in pages:
        page_id = page["id"]
        # Optional: fetch page title
        title = "Untitled"
        props = page.get("properties", {})
        for prop in props.values():
            if prop.get("type") == "title":
                title = "".join(t["plain_text"] for t in prop["title"])
                break

        blocks = fetch_blocks(page_id)
        text = extract_text(blocks)
        all_texts.append((title, text))
        sleep(0.2)  # to avoid rate limiting

    return all_texts

def fetch_page_content(page_id):
    all_text = []

    def recurse_blocks(block_id):
        response = notion.blocks.children.list(block_id=block_id)
        for block in response['results']:
            if 'paragraph' in block['type']:
                texts = block['paragraph']['text']
                for t in texts:
                    all_text.append(t['plain_text'])
            # handle other block types if needed (headings, lists, etc)
            # fetch children recursively if has_children:
            if block.get('has_children'):
                recurse_blocks(block['id'])

    recurse_blocks(page_id)
    return "\n".join(all_text)
