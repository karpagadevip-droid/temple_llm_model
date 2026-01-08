# Temple Expert RAG - Complete Colab Setup
# Clone entire project from GitHub and test RAG system

# =============================================================================
# CELL 1: Clone Repository from GitHub
# =============================================================================
!git clone https://github.com/karpagadevip-droid/temple_llm_model.git
%cd temple_llm_model

# Verify files
!ls -la

# =============================================================================
# CELL 2: Install Dependencies
# =============================================================================
!pip install -q unsloth transformers accelerate bitsandbytes python-dotenv tavily-python

# =============================================================================
# CELL 3: Set Environment Variables
# =============================================================================
import os

# IMPORTANT: Replace with your actual Tavily API key
TAVILY_API_KEY = "tvly-your-key-here"

# Create .env file
with open('.env', 'w') as f:
    f.write(f'TAVILY_API_KEY={TAVILY_API_KEY}\n')
    f.write('HUGGINGFACE_MODEL_PATH=Karpagadevi/llama-3-temple-expert\n')

print("✅ Environment configured")
print(f"   Tavily API Key: {TAVILY_API_KEY[:10]}...")
print(f"   Model: Karpagadevi/llama-3-temple-expert")

# =============================================================================
# CELL 4: Test Model Loading
# =============================================================================
from model_loader import TempleModelLoader

print("=" * 70)
print("TEST 1: Loading Fine-Tuned Model from Hugging Face")
print("=" * 70)
print("\nThis will take 2-3 minutes on first run...")
print("Model: Karpagadevi/llama-3-temple-expert (60 steps)")
print()

loader = TempleModelLoader(model_name="Karpagadevi/llama-3-temple-expert")
model, tokenizer = loader.load_model()

print("\n✅ Model loaded successfully!")
print("\nTesting query: 'Tell me about Meenakshi Temple'")
print()

response = loader.generate_response("Tell me about Meenakshi Temple", max_length=256)
print(f"Model Response:\n{response}")

# =============================================================================
# CELL 5: Test Tavily Search
# =============================================================================
from tavily_search import TavilySearcher

print("=" * 70)
print("TEST 2: Tavily AI Search")
print("=" * 70)
print()

searcher = TavilySearcher()
results = searcher.search_temple_tickets("Meenakshi Temple")

if results['success']:
    print("✅ Search successful!")
    print(f"\nAI Summary:\n{results['answer']}")
    print(f"\nSources found: {len(results['results'])}")
    
    # Show first source
    if results['results']:
        first = results['results'][0]
        print(f"\nTop Result:")
        print(f"  Title: {first['title']}")
        print(f"  Relevance: {first['score']:.2f}")
        print(f"  URL: {first['url']}")
else:
    print(f"❌ Search failed: {results.get('error')}")

# =============================================================================
# CELL 6: Test Complete RAG System
# =============================================================================
from rag_orchestrator import TempleRAG

print("=" * 70)
print("TEST 3: Complete RAG System (Model + Search)")
print("=" * 70)
print()

# Initialize RAG with model
print("Initializing RAG system...")
rag = TempleRAG(
    load_model=True,
    model_name="Karpagadevi/llama-3-temple-expert"
)

print("✅ RAG system ready!\n")

# Test different query types
test_queries = [
    {
        'query': "What is the ticket price for Meenakshi Temple?",
        'expected': 'search',
        'explanation': 'Real-time info → uses Tavily search'
    },
    {
        'query': "Tell me about the history of Meenakshi Temple",
        'expected': 'model',
        'explanation': 'Historical info → uses fine-tuned model'
    },
    {
        'query': "Tell me about Meenakshi Temple and how to visit",
        'expected': 'hybrid',
        'explanation': 'Both needed → uses model + search'
    }
]

for i, item in enumerate(test_queries, 1):
    print("\n" + "=" * 70)
    print(f"DEMO {i}/3: {item['explanation']}")
    print("=" * 70)
    print()
    
    result = rag.generate_response(item['query'])
    
    print(f"Strategy: {result['strategy']} (expected: {item['expected']})")
    print(f"Source: {result['source']}")
    print(f"\nResponse (first 400 chars):")
    print(result['response'][:400] + "..." if len(result['response']) > 400 else result['response'])
    print()

# =============================================================================
# CELL 7: Show Usage Statistics
# =============================================================================
stats = rag.get_stats()
tavily_stats = stats['tavily_usage']

print("\n" + "=" * 70)
print("USAGE STATISTICS")
print("=" * 70)
print(f"Tavily Searches Used: {tavily_stats['searches_used']}/{tavily_stats['free_tier_limit']}")
print(f"Remaining: {tavily_stats['remaining']} ({100-tavily_stats['percentage_used']:.1f}%)")
print(f"Model Loaded: {stats['model_loaded']}")
print("=" * 70)

print("\n✅ All tests complete!")
print("\nNext: Try your own queries in the cell below!")

# =============================================================================
# CELL 8: Interactive Testing
# =============================================================================
# Try your own queries!

query = input("Ask about a temple: ")
print()

result = rag.generate_response(query)

print(f"\n{'='*70}")
print(f"Strategy: {result['strategy']}")
print(f"Source: {result['source']}")
print(f"\nResponse:\n{result['response']}")
print('='*70)

# =============================================================================
# CELL 9: Compare Models (Run after 600-step model is ready)
# =============================================================================
# Uncomment and run this after your 600-step model is uploaded

# print("Comparing 60-step vs 600-step models...")
# print()

# # Test query
# test_query = "Tell me about Meenakshi Temple"

# # 60-step model
# print("Loading 60-step model...")
# rag_60 = TempleRAG(load_model=True, model_name="Karpagadevi/llama-3-temple-expert")
# response_60 = rag_60.generate_response(test_query)

# # 600-step model (update name when ready)
# print("Loading 600-step model...")
# rag_600 = TempleRAG(load_model=True, model_name="Karpagadevi/llama-3-temple-expert-600")
# response_600 = rag_600.generate_response(test_query)

# # Compare
# print("\n" + "="*70)
# print("60-STEP MODEL:")
# print("="*70)
# print(response_60['response'])

# print("\n" + "="*70)
# print("600-STEP MODEL:")
# print("="*70)
# print(response_600['response'])

# print("\n" + "="*70)
# print("Which one is better? 👆")
# print("="*70)
