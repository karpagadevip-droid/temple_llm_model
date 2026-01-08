# Temple Expert RAG - Colab Test Notebook
# Tests the complete RAG system with fine-tuned model + Tavily search

## Setup Instructions:

### 1. Upload These Files to Colab:
- `tavily_search.py`
- `rag_orchestrator.py`
- `model_loader.py`
- `demo_with_model.py`

### 2. Create a `.env` file in Colab with:
```
TAVILY_API_KEY=your_tavily_key_here
HUGGINGFACE_MODEL_PATH=Karpagadevi/llama-3-temple-expert
```

### 3. Run the cells below in order

---

## Cell 1: Install Dependencies

```python
!pip install -q unsloth transformers accelerate bitsandbytes python-dotenv tavily-python
```

## Cell 2: Verify Files Uploaded

```python
import os

required_files = [
    'tavily_search.py',
    'rag_orchestrator.py', 
    'model_loader.py',
    'demo_with_model.py',
    '.env'
]

print("Checking files...")
for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} - MISSING! Please upload.")
```

## Cell 3: Test Model Loading Only

```python
from model_loader import TempleModelLoader

print("Loading model from Hugging Face...")
print("(This will take 2-3 minutes on first run)")
print()

loader = TempleModelLoader(model_name="Karpagadevi/llama-3-temple-expert")
model, tokenizer = loader.load_model()

print("\n✅ Model loaded successfully!")
print("\nTesting with a query...")

response = loader.generate_response("Tell me about Meenakshi Temple")
print(f"\nModel Response:\n{response}")
```

## Cell 4: Test Complete RAG System

```python
from rag_orchestrator import TempleRAG

print("Initializing complete RAG system...")
print("(Model + Search)")
print()

rag = TempleRAG(
    load_model=True,
    model_name="Karpagadevi/llama-3-temple-expert"
)

print("✅ RAG ready!\n")

# Test queries
queries = [
    "What is the ticket price for Meenakshi Temple?",  # Search
    "Tell me about the history of Meenakshi Temple",   # Model
    "Tell me about Meenakshi Temple and how to visit"  # Hybrid
]

for i, query in enumerate(queries, 1):
    print(f"\n{'='*70}")
    print(f"Query {i}: {query}")
    print('='*70)
    
    result = rag.generate_response(query)
    
    print(f"\nStrategy: {result['strategy']}")
    print(f"Source: {result['source']}")
    print(f"\nResponse:\n{result['response'][:300]}...")
    print()
```

## Cell 5: Interactive Testing

```python
# Test your own queries!

query = input("Ask about a temple: ")
result = rag.generate_response(query)

print(f"\nStrategy: {result['strategy']}")
print(f"Source: {result['source']}")
print(f"\nResponse:\n{result['response']}")
```

---

## Expected Results:

### Query 1 (Ticket Price):
- Strategy: `search`
- Source: `tavily_search`
- Response: Real-time pricing info from web

### Query 2 (History):
- Strategy: `model`
- Source: `fine_tuned_model`
- Response: Historical info from your trained model

### Query 3 (Combined):
- Strategy: `hybrid`
- Source: `hybrid`
- Response: Both model knowledge + live search

---

## Troubleshooting:

### Error: "Tavily API key not found"
- Make sure `.env` file is uploaded
- Check `TAVILY_API_KEY` is set correctly

### Error: "Model not found"
- Check model name: `Karpagadevi/llama-3-temple-expert`
- Verify model is public on Hugging Face

### Slow responses on CPU
- Enable GPU: Runtime → Change runtime type → T4 GPU
- Restart runtime and run again

---

## Files Needed in Colab:

1. ✅ `tavily_search.py`
2. ✅ `rag_orchestrator.py`
3. ✅ `model_loader.py`
4. ✅ `demo_with_model.py`
5. ✅ `.env` (with your Tavily API key)

**Total: 5 files**

Upload these to Colab and run the cells above!
