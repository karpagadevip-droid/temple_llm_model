"""
Add these cells to your existing Temple_AI_Model.ipynb notebook
Copy and paste each cell into your Colab notebook
"""

# =============================================================================
# NEW SECTION: RAG System Testing (Add after your fine-tuning cells)
# =============================================================================

# Cell: Install RAG Dependencies
"""
!pip install -q tavily-python python-dotenv
"""

# Cell: Upload RAG Files
"""
from google.colab import files
import os

print("Upload these 4 files:")
print("1. tavily_search.py")
print("2. rag_orchestrator.py")
print("3. model_loader.py")
print("4. demo_with_model.py")
print()

uploaded = files.upload()
print(f"\n✅ Uploaded {len(uploaded)} files")
"""

# Cell: Set Tavily API Key
"""
import os

# Replace with your actual Tavily API key
TAVILY_API_KEY = "tvly-your-key-here"

# Create .env file
with open('.env', 'w') as f:
    f.write(f'TAVILY_API_KEY={TAVILY_API_KEY}\\n')
    f.write('HUGGINGFACE_MODEL_PATH=Karpagadevi/llama-3-temple-expert\\n')

print("✅ Environment configured")
"""

# Cell: Test 1 - Model Loading
"""
from model_loader import TempleModelLoader

print("=" * 70)
print("TEST 1: Loading Fine-Tuned Model")
print("=" * 70)
print()

loader = TempleModelLoader(model_name="Karpagadevi/llama-3-temple-expert")
model, tokenizer = loader.load_model()

print("\\n✅ Model loaded!")
print("\\nTesting query: 'Tell me about Meenakshi Temple'")
print()

response = loader.generate_response("Tell me about Meenakshi Temple", max_length=256)
print(f"Model Response:\\n{response}")
"""

# Cell: Test 2 - Search Only
"""
from tavily_search import TavilySearcher

print("=" * 70)
print("TEST 2: Tavily Search")
print("=" * 70)
print()

searcher = TavilySearcher()
results = searcher.search_temple_tickets("Meenakshi Temple")

if results['success']:
    print("✅ Search successful!")
    print(f"\\nAI Summary: {results['answer']}")
    print(f"\\nSources found: {len(results['results'])}")
else:
    print(f"❌ Search failed: {results.get('error')}")
"""

# Cell: Test 3 - Complete RAG System
"""
from rag_orchestrator import TempleRAG

print("=" * 70)
print("TEST 3: Complete RAG System (Model + Search)")
print("=" * 70)
print()

# Initialize with model
rag = TempleRAG(
    load_model=True,
    model_name="Karpagadevi/llama-3-temple-expert"
)

print("✅ RAG system ready!\\n")

# Test different query types
test_queries = [
    ("What is the ticket price for Meenakshi Temple?", "search"),
    ("Tell me about the history of Meenakshi Temple", "model"),
    ("Tell me about Meenakshi Temple and how to visit", "hybrid")
]

for query, expected in test_queries:
    print("\\n" + "=" * 70)
    print(f"Query: {query}")
    print("=" * 70)
    
    result = rag.generate_response(query)
    
    print(f"\\nStrategy: {result['strategy']} (expected: {expected})")
    print(f"Source: {result['source']}")
    print(f"\\nResponse (first 300 chars):")
    print(result['response'][:300] + "...")
    print()

# Show stats
stats = rag.get_stats()
print("\\n" + "=" * 70)
print("Usage Statistics:")
print("=" * 70)
print(f"Tavily searches: {stats['tavily_usage']['searches_used']}/1000")
print(f"Model loaded: {stats['model_loaded']}")
"""

# Cell: Test 4 - Interactive Testing
"""
# Try your own queries!

query = input("Ask about a temple: ")
result = rag.generate_response(query)

print(f"\\n{'='*70}")
print(f"Strategy: {result['strategy']}")
print(f"Source: {result['source']}")
print(f"\\nResponse:\\n{result['response']}")
print('='*70)
"""

# Cell: Compare 60-step vs 600-step Models
"""
# After your 600-step model is ready, run this to compare

print("Comparing model versions...")
print()

# Test with 60-step model
rag_60 = TempleRAG(load_model=True, model_name="Karpagadevi/llama-3-temple-expert")
response_60 = rag_60.generate_response("Tell me about Meenakshi Temple")

# Test with 600-step model (update name when ready)
# rag_600 = TempleRAG(load_model=True, model_name="Karpagadevi/llama-3-temple-expert-600")
# response_600 = rag_600.generate_response("Tell me about Meenakshi Temple")

print("60-step model response:")
print(response_60['response'][:300])
print()

# print("600-step model response:")
# print(response_600['response'][:300])
"""
