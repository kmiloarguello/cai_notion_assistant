# test_fetch_db.py

from notion_fetcher.fetch import fetch_all_texts_from_database

import os
from dotenv import load_dotenv

load_dotenv()  # Load env variables from .env

def main():
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not database_id:
        print("❌ ERROR: NOTION_DATABASE_ID is not set in the .env file.")
        return

    print(f"📥 Fetching content from Notion database: {database_id}\n")

    pages = fetch_all_texts_from_database(database_id)
    for title, content in pages:
        print(f"\n=== {title} ===\n")
        print(content[:500])  # Show first 500 chars of content

if __name__ == "__main__":
    main()
