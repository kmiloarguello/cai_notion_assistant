# Notion AI Assistant 🤖

An intelligent AI agent that retrieves and processes data from your Notion database using embeddings and RAG (Retrieval-Augmented Generation) to answer questions about your team's knowledge base.

## 🎯 Features

- **Smart Retrieval**: Uses embedding-based search to find relevant information
- **AI-Powered Answers**: Leverages OpenAI GPT models for contextual responses
- **Notion Integration**: Seamlessly fetches content from your Notion databases
- **Interactive CLI**: Easy-to-use command-line interface
- **Caching**: Efficient embedding storage for fast queries
- **Rate Limiting**: Built-in protection against API limits

## 🏗️ Architecture

```
User → VS Code / Terminal → Local Agent → Notion API
                                  ↓
                    Embedding-based search / RAG
                                  ↓
                  LLM (GPT-4 or other models)
                                  ↓
                     Contextual Answer to User
```

## 📁 Project Structure

```
notion_ai_assistant/
├── notion_fetcher/          # Notion API integration
│   ├── __init__.py
│   └── fetch.py            # Fetch pages and content from Notion
├── indexing/               # Content processing and embedding
│   ├── __init__.py
│   └── embed.py           # Create embeddings from Notion content
├── rag_agent/             # RAG pipeline
│   └── answer.py          # Retrieval and answer generation
├── app.py                 # Main application entry point
├── run.py                 # Simple runner script
├── setup.py               # Installation and setup script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Setup

```bash
# Clone or download the project
cd cai_notion_assistant

# Run the setup script
python setup.py
```

### 2. Configure Environment

Create a `.env` file with your API keys:

```env
# Get from https://www.notion.so/my-integrations
NOTION_API_KEY=your_notion_api_key_here

# Your Notion database ID (from the URL)
NOTION_DATABASE_ID=your_notion_database_id_here

# Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Assistant

```bash
python app.py
# or
python run.py
```

## 🔧 Usage

### First-Time Setup
1. **Index your Notion database** (Option 1 in menu)
   - This fetches all pages from your Notion database
   - Creates embeddings for efficient search
   - Saves embeddings locally for fast access

2. **Ask questions** (Option 2 in menu)
   - Enter interactive mode
   - Ask natural language questions about your content

### Example Questions

- "What is our standard for writing unit tests?"
- "What's the deployment procedure?"
- "What does the analytics.js file do?"
- "Are there any best practices for API error handling in our team?"

## 📋 Menu Options

1. **🔄 Index Notion Database** - Create/update embeddings from your Notion content
2. **💬 Ask Questions** - Interactive Q&A mode
3. **📊 Show Statistics** - View information about indexed content
4. **🧪 Test Single Question** - Quick test mode
5. **🚪 Exit** - Close the application

## 🔑 Getting API Keys

### Notion API Key
1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Give it a name and select your workspace
4. Copy the "Internal Integration Token"
5. **Important**: Share your database with the integration

### Notion Database ID
1. Open your Notion database in a browser
2. Copy the ID from the URL: `https://www.notion.so/workspace/DATABASE_ID?v=...`
3. The DATABASE_ID is the long string of characters

### OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new secret key
3. Copy the key (starts with `sk-`)

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NOTION_API_KEY` | Your Notion integration token | Yes |
| `NOTION_DATABASE_ID` | ID of the Notion database to index | Yes |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Customization

You can modify the following in the code:

- **Embedding Model**: Change in `embed.py` (default: `text-embedding-3-small`)
- **LLM Model**: Change in `answer.py` (default: `gpt-4o-mini`)
- **Chunk Size**: Modify `max_length` in `chunk_text()` function
- **Number of Retrieved Chunks**: Change `top_k` parameter

## 🛠️ Dependencies

- `notion-client` - Notion API integration
- `openai` - OpenAI API client
- `numpy` - Numerical computations
- `python-dotenv` - Environment variable management

## 🚨 Important Notes

### Rate Limits
- **Notion API**: Built-in rate limiting with exponential backoff
- **OpenAI API**: 0.1s delay between embedding requests

### Content Processing
- Supports various Notion block types (paragraphs, headings, lists, code, etc.)
- Automatically handles pagination for large databases
- Skips empty pages and very short chunks

### Performance Tips
- Index your database during off-peak hours
- For large databases, consider running incremental updates
- Embeddings are cached locally for fast retrieval

## 🔍 Troubleshooting

### Common Issues

1. **"No embeddings found"**
   - Run option 1 to index your database first

2. **"Import errors"**
   - Run `pip install -r requirements.txt`

3. **"Notion API errors"**
   - Check if your integration has access to the database
   - Verify your API key is correct

4. **"Empty responses"**
   - Ensure your Notion pages have content
   - Check if the database ID is correct

### Error Messages

- **❌ Missing environment variables**: Update your `.env` file
- **❌ No pages found**: Check database ID and integration permissions
- **❌ Failed to embed**: Check OpenAI API key and quota

## 📈 Advanced Usage

### Batch Processing
```python
# For large databases, you might want to process in batches
# Modify the chunk_text function to handle larger texts
```

### Custom Models
```python
# Use different models by changing the model parameter
# In answer.py, modify the generate_answer function
response = client.chat.completions.create(
    model="gpt-4",  # or "gpt-3.5-turbo"
    # ...
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify as needed.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your API keys and permissions
3. Check the console output for specific error messages

---

**Happy querying! 🎉**
