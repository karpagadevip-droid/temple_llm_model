# Temple Expert RAG System - Usage Guide

## 🎯 What is RAG?

**RAG (Retrieval Augmented Generation)** is a technique that combines:
- **Frozen Knowledge**: Your fine-tuned model's learned information
- **Live Knowledge**: Real-time web search results

This solves the hallucination problem where models make up facts they don't know.

## 🔑 Setup Instructions

### Step 1: Get Tavily API Key

1. Sign up at **https://tavily.com/**
2. Navigate to your dashboard
3. Copy your API key
4. **Free tier**: 1,000 searches/month (perfect for development!)

### Step 2: Configure Environment

Create a `.env` file in your project directory:

```bash
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ IMPORTANT**: Never commit your `.env` file to Git! It's already in `.gitignore`.

### Step 3: Install Dependencies

```bash
pip install tavily-python python-dotenv
```

## 🏗️ How the RAG System Works

### Query Classification

The system automatically classifies your query into three categories:

| Category | When Used | Example |
|----------|-----------|---------|
| **Model** | Historical/cultural questions | "Tell me about Meenakshi Temple history" |
| **Search** | Real-time information | "What is the ticket price?" |
| **Hybrid** | Both needed | "Tell me about the temple and how to visit" |

### Classification Keywords

**Search Keywords** (triggers live search):
- `ticket`, `price`, `cost`, `fee`, `entry`
- `timing`, `time`, `open`, `close`, `hours`
- `how to reach`, `directions`, `location`, `address`
- `current`, `now`, `today`, `latest`

**Model Keywords** (uses fine-tuned model):
- `history`, `built`, `architecture`, `deity`
- `significance`, `legend`, `story`, `mythology`
- `festival`, `ritual`, `tradition`, `culture`

## 💻 Usage Examples

### Example 1: Basic Search

```python
from tavily_search import TavilySearcher

# Initialize searcher
searcher = TavilySearcher()

# Search for ticket information
results = searcher.search_temple_tickets("Meenakshi Temple")

# Format results
formatted = searcher.format_search_results(results)
print(formatted)
```

### Example 2: RAG Orchestrator

```python
from rag_orchestrator import TempleRAG

# Initialize RAG system
rag = TempleRAG()

# Ask a question
response = rag.generate_response("What is the ticket price for Meenakshi Temple?")

print(response['response'])
print(f"Source: {response['source']}")  # 'search', 'model', or 'hybrid'
```

### Example 3: Check Usage

```python
# Get usage statistics
stats = searcher.get_usage_stats()
print(f"Searches used: {stats['searches_used']}/{stats['free_tier_limit']}")
print(f"Remaining: {stats['remaining']}")
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Run all tests
python test_rag.py

# Run specific tests
python test_rag.py --test-search
python test_rag.py --test-classification
python test_rag.py --test-e2e
```

## 📊 Understanding Tavily Responses

Tavily returns AI-optimized results with:

1. **AI Summary**: A concise answer to your query
2. **Sources**: Relevant web pages with:
   - Title
   - Content snippet
   - URL
   - Relevance score (0.0 to 1.0)

Example response structure:
```json
{
  "answer": "Meenakshi Temple entry fee is ₹50 for adults...",
  "results": [
    {
      "title": "Meenakshi Temple Timings and Entry Fee",
      "content": "The temple is open from 5 AM to 12:30 PM...",
      "url": "https://example.com/meenakshi-temple",
      "score": 0.95
    }
  ]
}
```

## 🔧 Troubleshooting

### Error: "Tavily API key not found"

**Solution**: Make sure you have:
1. Created a `.env` file in the project directory
2. Added `TAVILY_API_KEY=your_key_here`
3. Installed `python-dotenv`: `pip install python-dotenv`

### Error: "tavily-python library not found"

**Solution**: Install the library:
```bash
pip install tavily-python
```

### Search returns no results

**Possible causes**:
1. Query is too specific or misspelled
2. API rate limit reached (1,000/month on free tier)
3. Network connectivity issues

**Solution**: Try a broader query or check your internet connection.

### Warning: "90% of free searches used"

**Solution**: 
- Monitor your usage with `searcher.get_usage_stats()`
- Consider upgrading to a paid plan if needed
- Implement caching to reduce duplicate searches

## 🎓 GenAI Concepts (Day 4 Learning)

### RAG vs. Fine-Tuning

| Aspect | Fine-Tuning | RAG |
|--------|-------------|-----|
| **Knowledge** | Frozen at training time | Real-time from web |
| **Cost** | High (GPU training) | Low (API calls) |
| **Updates** | Requires retraining | Automatic |
| **Best For** | Domain expertise | Current information |

### Interview Question: "When would you use RAG vs. Fine-Tuning?"

**Answer**: 
- **Fine-tune** when you need the model to learn domain-specific language, style, or reasoning patterns
- **Use RAG** when you need access to current information or a large knowledge base
- **Combine both** (like we're doing!) for the best results

### Key Concept: Grounding

**Grounding** means connecting the model's output to verifiable sources. RAG provides grounding by:
1. Citing sources (URLs)
2. Showing relevance scores
3. Allowing users to verify information

This reduces hallucinations and builds trust!

## 📚 Next Steps (Day 5)

After mastering RAG, you'll learn:
- **Agent Architecture**: Building a `TempleAgent` class
- **ReAct Pattern**: Reasoning + Acting in a loop
- **Tool Selection**: Teaching the agent when to search vs. when to use the model

## 🆘 Need Help?

- Tavily Documentation: https://docs.tavily.com/
- Python dotenv: https://pypi.org/project/python-dotenv/
- Check `test_rag.py` for working examples
