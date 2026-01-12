# Testing Temple Agent in Colab

## Quick Start

### Option 1: Run Python Script (Recommended)

```python
# Cell 1: Setup
!git clone https://github.com/karpagadevip-droid/temple_llm_model.git
%cd temple_llm_model
!pip install -q unsloth transformers accelerate bitsandbytes python-dotenv tavily-python

# Cell 2: Set API Key
%%writefile .env
TAVILY_API_KEY=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

# Cell 3: Run Test
!python test_agent_colab.py
```

### Option 2: Interactive Testing

```python
# After setup (cells 1-2 above):

from temple_agent import TempleAgent
from rag_orchestrator import TempleRAG

# Load model
rag = TempleRAG(
    load_model=True,
    model_name="Karpagadevi/llama-3-temple-expert"
)

# Create agent
agent = TempleAgent(rag_system=rag, verbose=True)

# Test queries
response = agent.respond("What is the ticket price for Meenakshi Temple?")
print(response['response'])
```

---

## What Gets Tested

✅ **Search Strategy** - Tavily API for real-time info  
✅ **Model Strategy** - Fine-tuned Llama for historical facts  
✅ **Hybrid Strategy** - Combined approach  
✅ **Quality Assessment** - 1-10 scoring  
✅ **Conversation Memory** - deque with auto-limiting  
✅ **Tool Selection** - Intelligent routing  

---

## Expected Output

```
Temple Agent - Complete Test with Model
======================================================================

Loading fine-tuned model from Hugging Face...
Model: Karpagadevi/llama-3-temple-expert
This may take 2-3 minutes on first run...

[OK] Model loaded successfully!

======================================================================
Query 1: What is the ticket price for Meenakshi Temple?
Expected strategy: search
----------------------------------------------------------------------

Strategy: search
Temple: Meenakshi Temple
Confidence: 95%
Quality: 10/10
Source: tavily_search

Answer: Entry fee is Rs 100. Opens at 4 AM...

[OK] Strategy matches expectation!

======================================================================
Query 2: Tell me about the history of Meenakshi Temple
Expected strategy: model
----------------------------------------------------------------------

Strategy: model
Temple: Meenakshi Temple
Confidence: 95%
Quality: 8/10
Source: fine_tuned_model

Answer: Meenakshi Temple is a historic Hindu temple...

[OK] Strategy matches expectation!

======================================================================
Query 3: Tell me about Meenakshi Temple and how to visit
Expected strategy: hybrid
----------------------------------------------------------------------

Strategy: hybrid
Temple: Meenakshi Temple
Confidence: 85%
Quality: 10/10
Source: hybrid

Answer: **Historical Information:**
Meenakshi Temple is a historic temple...
**Practical Information:**
Entry fee is Rs 100...

[OK] Strategy matches expectation!

======================================================================
Agent Statistics
======================================================================
Total queries: 3
Strategies used: {'search': 1, 'model': 1, 'hybrid': 1}
Temples discussed: ['Meenakshi Temple']

Tavily searches: 2/1000

Test Complete!
```

---

## Time Estimate

- **Setup** (cells 1-2): ~2 minutes
- **Model download** (first time): ~2-3 minutes
- **Test execution**: ~1-2 minutes

**Total**: ~5-7 minutes

---

## Troubleshooting

### GPU Limit Error
If you hit GPU limit, wait 12-24 hours or use CPU:
- Runtime → Change runtime type → None (CPU)
- Test will be slower but still works

### Model Not Found
Check model name is correct:
- `Karpagadevi/llama-3-temple-expert`
- Verify it's public on Hugging Face

### Tavily Error
Make sure API key is set in `.env` file

---

## Files Used

All files are in GitHub, automatically cloned:
- `test_agent_colab.py` - This test script
- `temple_agent.py` - Agent with ReAct pattern
- `rag_orchestrator.py` - RAG system
- `model_loader.py` - Model loading
- `tavily_search.py` - Search integration

**No manual uploads needed!** 🎉
