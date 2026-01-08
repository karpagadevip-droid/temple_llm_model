# Temple Expert RAG Testing - Colab Notebook
# Copy these cells into a new Colab notebook to test the RAG system

# ==============================================================================
# CELL 1: Setup - Clone Repository
# ==============================================================================
!git clone https://github.com/karpagadevip-droid/temple_llm_model.git
%cd temple_llm_model
!ls -la

# ==============================================================================
# CELL 2: Install Dependencies
# ==============================================================================
!pip install -q unsloth transformers accelerate bitsandbytes python-dotenv tavily-python

# ==============================================================================
# CELL 3: Set Environment Variables (IMPORTANT: Add your keys!)
# ==============================================================================
%%writefile .env
TAVILY_API_KEY=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
HUGGINGFACE_TOKEN=hf_your_token_here

# Verify .env file created
!cat .env

# ==============================================================================
# CELL 4: Quick Test - Search Only (No Model)
# ==============================================================================
# This tests Tavily search without loading the model (fast!)

from dotenv import load_dotenv
load_dotenv()

from tavily_search import TavilySearcher

print("Testing Tavily Search...")
searcher = TavilySearcher()
results = searcher.search_temple_tickets("Meenakshi Temple")

if results['success']:
    print("\n✅ Search working!")
    print(f"\nAI Summary:\n{results['answer']}")
else:
    print(f"\n❌ Search failed: {results.get('error')}")

# ==============================================================================
# CELL 5: Test Complete RAG System (Model + Search)
# ==============================================================================
# This loads the model from Hugging Face and tests the full RAG system
# WARNING: First run takes 2-3 minutes to download model (~4GB)

!python demo_with_model.py

# ==============================================================================
# CELL 6: Interactive Testing (Optional)
# ==============================================================================
# Test with your own queries

from rag_orchestrator import TempleRAG

# Initialize RAG (model already loaded if you ran Cell 5)
rag = TempleRAG(
    load_model=True,
    model_name="Karpagadevi/llama-3-temple-expert"
)

# Try your own query
query = input("Ask about a temple: ")
result = rag.generate_response(query)

print(f"\n{'='*70}")
print(f"Strategy: {result['strategy']}")
print(f"Source: {result['source']}")
print(f"\nResponse:\n{result['response']}")
print('='*70)

# ==============================================================================
# CELL 7: Compare 60-step vs 600-step Models (After 600-step is ready)
# ==============================================================================
# Run this after your 600-step model finishes training

from rag_orchestrator import TempleRAG

test_query = "Tell me about Meenakshi Temple"

print("Loading 60-step model...")
rag_60 = TempleRAG(load_model=True, model_name="Karpagadevi/llama-3-temple-expert")
result_60 = rag_60.generate_response(test_query)

print("\nLoading 600-step model...")
rag_600 = TempleRAG(load_model=True, model_name="Karpagadevi/llama-3-temple-expert-600")
result_600 = rag_600.generate_response(test_query)

# Compare
print("\n" + "="*70)
print("60-STEP MODEL RESPONSE:")
print("="*70)
print(result_60['response'])

print("\n" + "="*70)
print("600-STEP MODEL RESPONSE:")
print("="*70)
print(result_600['response'])

print("\n" + "="*70)
print("Which one is better? 👆")
print("="*70)
