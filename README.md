# Notion AI Assistant 🤖

An intelligent AI agent that retrieves and processes data from your Notion database using embeddings and RAG (Retrieval-Augmented Generation) to answer questions about your team's knowledge base.

## 🎯 Features

- **Smart Retrieval**: Uses embedding-based search to find relevant information
- **AI-Powered Answers**: Leverages OpenAI GPT models or Groq for contextual responses
- **Local Embeddings**: Supports both OpenAI and local sentence-transformers models
- **Notion Integration**: Seamlessly fetches content from your Notion databases
- **Interactive CLI**: Easy-to-use command-line interface
- **Persistent Caching**: Efficient embedding storage for fast queries
- **Rate Limiting**: Built-in protection against API limits
- **Auto-Fallback**: Automatically switches to Groq when OpenAI quota is exceeded

## 🏗️ Architecture

```
User → VS Code / Terminal → Local Agent → Notion API
                                  ↓
                    Embedding-based search / RAG
                                  ↓
          LLM (Local like Mistral, or remote like GPT-4/Groq)
                                  ↓
                     Contextual Answer to User
```

## 📁 Project Structure

```
cai_notion_assistant/
├── notion_fetcher/              # Notion API integration
│   ├── __init__.py
│   └── fetch.py                # Fetches pages and content from Notion
├── indexing/                   # Content processing and embedding
│   ├── __init__.py
│   ├── embed.py               # Creates embeddings from Notion content
│   └── embedding_providers.py # Local and remote embedding providers
├── rag_agent/                 # RAG pipeline implementation
│   ├── __init__.py
│   ├── answer.py             # Retrieval and answer generation
│   └── llm_providers.py      # OpenAI and Groq LLM providers
├── app.py                     # Main application entry point
├── run.py                     # Simple runner script
├── setup.py                   # Installation and setup script
├── test_openai.py            # OpenAI API connection test
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create this)
├── .gitignore
└── README.md
```

## 📄 File Documentation

### Core Application Files

#### `app.py`

- **Purpose**: Main application entry point with interactive CLI
- **Features**:
  - Menu-driven interface for all operations
  - Database indexing and question answering
  - Statistics display and testing modes
  - Error handling and user guidance
- **Key Functions**:
  - `main()`: Main application loop
  - `display_menu()`: Shows available options
  - `handle_*()`: Individual menu option handlers

#### `run.py`

- **Purpose**: Simple script to run the application
- **Usage**: `python run.py` - alternative to `python app.py`

#### `setup.py`

- **Purpose**: Automated setup and dependency installation
- **Features**:
  - Installs required Python packages
  - Creates `.env` template if it doesn't exist
  - Validates environment setup
  - Provides setup guidance

### Notion Integration

#### `notion_fetcher/fetch.py`

- **Purpose**: Handles all Notion API interactions
- **Key Classes**:
  - `NotionFetcher`: Main class for Notion operations
- **Key Methods**:
  - `fetch_database_pages()`: Retrieves all pages from a database
  - `extract_page_content()`: Converts Notion blocks to text
  - `_extract_block_content()`: Handles different block types
- **Features**:
  - Rate limiting with exponential backoff
  - Comprehensive block type support (paragraphs, headings, lists, code, etc.)
  - Pagination handling for large databases
  - Robust error handling

### Embedding and Indexing

#### `indexing/embed.py`

- **Purpose**: Creates and manages embeddings for text content
- **Key Classes**:
  - `EmbeddingManager`: Manages embedding creation and storage
- **Key Methods**:
  - `create_embeddings()`: Processes pages and creates embeddings
  - `chunk_text()`: Splits text into manageable chunks
  - `save_embeddings()`: Persists embeddings to disk
  - `load_embeddings()`: Loads cached embeddings
- **Features**:
  - Text chunking with overlap for better context
  - Multiple embedding provider support
  - Persistent storage using pickle
  - Progress tracking for large datasets

#### `indexing/embedding_providers.py`

- **Purpose**: Provides multiple embedding model options
- **Key Functions**:
  - `get_openai_embedding()`: Uses OpenAI's embedding models
  - `get_local_embedding()`: Uses sentence-transformers locally
  - `get_embedding()`: Unified interface with fallback
- **Features**:
  - OpenAI embedding API integration
  - Local sentence-transformers support
  - Automatic fallback between providers
  - Configurable model selection

### RAG Pipeline

#### `rag_agent/answer.py`

- **Purpose**: Implements the RAG (Retrieval-Augmented Generation) pipeline
- **Key Classes**:
  - `RAGAgent`: Main RAG pipeline orchestrator
- **Key Methods**:
  - `answer_question()`: Main question-answering pipeline
  - `retrieve_relevant_chunks()`: Finds most relevant content
  - `generate_answer()`: Creates contextual answers
- **Features**:
  - Cosine similarity-based retrieval
  - Configurable number of retrieved chunks
  - Context-aware answer generation
  - Multiple LLM provider support

#### `rag_agent/llm_providers.py`

- **Purpose**: Provides multiple LLM options for answer generation
- **Key Classes**:
  - `OpenAIProvider`: OpenAI GPT models
  - `GroqProvider`: Groq's fast inference models
- **Key Methods**:
  - `generate_answer()`: Generates contextual answers
  - `get_available_models()`: Lists available models
- **Features**:
  - Multiple LLM provider support
  - Automatic fallback between providers
  - Configurable model parameters
  - Robust error handling

### Testing and Utilities

#### `test_openai.py`

- **Purpose**: Tests OpenAI API connectivity
- **Features**:
  - API key validation
  - Connection testing
  - Response verification
  - Error diagnostics

## 🚀 Quick Start

### 1. Setup

```bash
# Navigate to project directory
cd cai_notion_assistant

# Run the automated setup
python setup.py

# Or install dependencies manually
pip install -r requirements.txt
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

# Get from https://console.groq.com/keys (optional, for fallback)
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the Assistant

```bash
python app.py
# or
python run.py
```

## 🔧 Usage

### Workflow

1. **Index your Notion database** (Option 1 in menu)

   - Fetches all pages from your Notion database
   - Creates embeddings for efficient search
   - Saves embeddings locally for fast access

2. **Ask questions** (Option 2 in menu)
   - Enter interactive mode
   - Ask natural language questions about your content
   - Get contextual answers based on your Notion content

### Example Questions

- "What is our standard for writing unit tests?"
- "What's the deployment procedure?"
- "What does the analytics.js file do?"
- "Are there any best practices for API error handling in our team?"
- "What are the key features of our product?"
- "How do we handle customer support escalations?"

## 📋 Menu Options

1. **🔄 Index Notion Database** - Create/update embeddings from your Notion content
2. **💬 Ask Questions** - Interactive Q&A mode with context retrieval
3. **📊 Show Statistics** - View information about indexed content
4. **🧪 Test Single Question** - Quick test mode for single questions
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

### Groq API Key (Optional)

1. Go to [Groq Console](https://console.groq.com/keys)
2. Create a new API key
3. Copy the key for fallback LLM usage

## ⚙️ Configuration

### Environment Variables

| Variable             | Description                        | Required |
| -------------------- | ---------------------------------- | -------- |
| `NOTION_API_KEY`     | Your Notion integration token      | Yes      |
| `NOTION_DATABASE_ID` | ID of the Notion database to index | Yes      |
| `OPENAI_API_KEY`     | Your OpenAI API key                | Yes      |
| `GROQ_API_KEY`       | Your Groq API key (fallback)       | No       |

### Customization Options

#### Embedding Models

- **OpenAI**: `text-embedding-3-small` (default), `text-embedding-3-large`
- **Local**: `all-MiniLM-L6-v2` (default), `all-mpnet-base-v2`

#### LLM Models

- **OpenAI**: `gpt-4o-mini` (default), `gpt-4`, `gpt-3.5-turbo`
- **Groq**: `mixtral-8x7b-32768`, `llama2-70b-4096`

#### Retrieval Parameters

- **Chunk Size**: 1000 characters (configurable in `embed.py`)
- **Overlap**: 200 characters between chunks
- **Top K**: 3 most relevant chunks retrieved

## 🛠️ Dependencies

### Core Dependencies

- `notion-client` - Notion API integration
- `openai` - OpenAI API client
- `groq` - Groq API client
- `sentence-transformers` - Local embedding models
- `numpy` - Numerical computations (downgraded for compatibility)
- `python-dotenv` - Environment variable management

### Installation

```bash
pip install -r requirements.txt
```

## 🚨 Important Notes

### Rate Limits

- **Notion API**: Built-in rate limiting with exponential backoff
- **OpenAI API**: 0.1s delay between embedding requests
- **Groq API**: Used as fallback when OpenAI quota exceeded

### Content Processing

- Supports various Notion block types:
  - Paragraphs, headings, bulleted/numbered lists
  - Code blocks, quotes, callouts
  - Tables, toggles, and more
- Automatically handles pagination for large databases
- Skips empty pages and very short chunks
- Preserves formatting context in embeddings

### Performance Optimization

- Embeddings are cached locally using pickle
- Incremental updates supported
- Parallel processing for large datasets
- Memory-efficient chunking strategy

## 🔍 Troubleshooting

### Common Issues

1. **"No embeddings found"**

   - Run option 1 to index your database first
   - Check if embedding files exist in the directory

2. **"Import errors"**

   - Run `pip install -r requirements.txt`
   - Check Python version compatibility (3.8+)

3. **"Notion API errors"**

   - Verify your integration has access to the database
   - Check if your API key is correct and active
   - Ensure database ID is valid

4. **"Empty responses"**

   - Ensure your Notion pages have content
   - Check if the database ID is correct
   - Verify pages are not empty or too short

5. **"Embedding errors"**
   - Check OpenAI API quota and billing
   - Try using local embeddings as fallback
   - Verify API key permissions

### Error Messages

- **❌ Missing environment variables**: Update your `.env` file
- **❌ No pages found**: Check database ID and integration permissions
- **❌ Failed to embed**: Check OpenAI API key and quota
- **❌ Import errors**: Install missing dependencies
- **❌ Rate limit exceeded**: Wait and retry, or use fallback providers

## 📈 Advanced Usage

### Batch Processing

```python
# For large databases, process in smaller batches
# Modify chunk_size in embed.py for memory optimization
```

### Custom Models

```python
# Use different embedding models
embedding = get_local_embedding(text, model_name="all-mpnet-base-v2")

# Use different LLM models
llm_provider = OpenAIProvider(model="gpt-4")
```

### Integration with VS Code

```bash
# Run from VS Code terminal
python app.py

# Or create a VS Code task in tasks.json
{
    "label": "Run Notion AI Assistant",
    "type": "shell",
    "command": "python app.py"
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Test thoroughly with different Notion databases
6. Submit a pull request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_openai.py

# Test with sample data
python app.py
```

## 📄 License

This project is open source. Feel free to use and modify as needed for your team's requirements.

## 🆘 Support

If you encounter issues:

1. **Check the troubleshooting section** above
2. **Verify your API keys and permissions**
3. **Check the console output** for specific error messages
4. **Review the logs** for detailed error information
5. **Test with smaller datasets** first

### Debug Mode

Add debug prints to understand the flow:

```python
# In app.py, add debugging
print(f"Debug: Loaded {len(embeddings)} embeddings")
```

## 🎯 Use Cases

### Team Knowledge Base

- Document standards and best practices
- Deployment procedures and runbooks
- Code documentation and architecture decisions
- Meeting notes and project updates

### Customer Support

- FAQ responses and troubleshooting guides
- Product feature documentation
- Support escalation procedures
- Customer feedback and insights

### Project Management

- Project requirements and specifications
- Timeline and milestone tracking
- Resource allocation and planning
- Retrospective notes and lessons learned

---

**Happy querying with your Notion AI Assistant! 🎉**

\*Built with ❤️ by CA_AI
