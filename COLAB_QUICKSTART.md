# Quick Start Guide - Running in Colab

## 🎯 Two Notebooks, Two Purposes

### Notebook 1: Training (600 steps)
**File**: `Temple_AI_Model.ipynb` (already in your GitHub)

**How to run**:
1. Open Colab: https://colab.research.google.com/
2. File → Open from GitHub
3. Enter: `karpagadevip-droid/temple_llm_model`
4. Select: `Temple_AI_Model.ipynb`
5. Add this cell at the top:
   ```python
   %%writefile .env
   HUGGINGFACE_TOKEN=hf_your_token_here
   ```
6. Run all cells
7. Model trains and uploads automatically!

---

### Notebook 2: Testing RAG System
**File**: Create new notebook in Colab

**How to run**:
1. Open Colab: https://colab.research.google.com/
2. Create new notebook
3. Copy cells from `TEST_RAG_COLAB.md`
4. Update your Tavily API key in Cell 3
5. Run cells 1-5 to test RAG system

---

## 📋 Step-by-Step: Testing RAG in Colab

### Step 1: Open Colab
Go to: https://colab.research.google.com/

### Step 2: Create New Notebook
Click: **File → New Notebook**

### Step 3: Copy These Cells

**Cell 1** - Clone repo:
```python
!git clone https://github.com/karpagadevip-droid/temple_llm_model.git
%cd temple_llm_model
```

**Cell 2** - Install packages:
```python
!pip install -q unsloth transformers accelerate bitsandbytes python-dotenv tavily-python
```

**Cell 3** - Set your Tavily key:
```python
%%writefile .env
TAVILY_API_KEY=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
```

**Cell 4** - Run RAG demo:
```python
!python demo_with_model.py
```

### Step 4: Run All Cells!
Click: **Runtime → Run all**

---

## ⏱️ Expected Time

- **Cell 1-3**: ~30 seconds (setup)
- **Cell 4**: 
  - First time: 2-3 minutes (downloads model)
  - After that: 1-2 minutes (model cached)

---

## 🎯 What You'll See

```
======================================================================
COMPLETE RAG SYSTEM - Model + Search Demo
======================================================================

Initializing RAG system...
Loading model: Karpagadevi/llama-3-temple-expert
[OK] Model loaded successfully!

======================================================================
DEMO 1/3: Real-time info - uses Tavily search
======================================================================

[Query] What is the ticket price for Meenakshi Temple?
[Strategy] search
[Temple] Meenakshi Temple

[Using Tavily search...]

[Response]
**AI Summary:**
Meenakshi Temple entry is free. Opens at 5 AM...

======================================================================
DEMO 2/3: Historical info - uses fine-tuned model
======================================================================

[Query] Tell me about the history of Meenakshi Temple
[Strategy] model
[Temple] Meenakshi Temple

[Using fine-tuned model...]

[Response]
Meenakshi Temple is a historic Dravidian temple...

======================================================================
DEMO 3/3: Both needed - uses model + search
======================================================================
...
```

---

## 🔧 Troubleshooting

### Error: "Tavily API key not found"
- Check Cell 3 - make sure you pasted your actual key
- Run Cell 3 again

### Error: "Model not found"
- Model name might be wrong
- Check: https://huggingface.co/Karpagadevi/llama-3-temple-expert

### Slow responses
- Enable GPU: Runtime → Change runtime type → T4 GPU
- Restart runtime and run again

---

## 🚀 Ready to Test?

1. Open Colab
2. Copy the 4 cells above
3. Update your Tavily key
4. Run all!

**That's it!** 🎉

---

## 📊 Files in GitHub

All these files are automatically available when you clone:

- ✅ `demo_with_model.py` - Main RAG demo
- ✅ `tavily_search.py` - Search module
- ✅ `rag_orchestrator.py` - RAG brain
- ✅ `model_loader.py` - Model loader
- ✅ `temples.json` - Training data
- ✅ `temples_with_refusals.json` - Augmented data

**No manual uploads needed!** Everything comes from GitHub.
