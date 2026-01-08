# Quick Test: Model Integration
# Tests if the model can be loaded and used with RAG

This is a simple test to verify the model integration works.

## What to Test:

### Option 1: Test Model Loading Only (Faster)

```bash
cd "d:\Devi Tech\temple-expert-rag"
python model_loader.py
```

**Expected**: Model downloads and generates a test response (may take 2-5 minutes first time)

### Option 2: Test Complete RAG System

```bash
cd "d:\Devi Tech\temple-expert-rag"
python demo_with_model.py
```

**Expected**: Shows 3 demos with model + search working together

## ⚠️ Important Notes:

1. **First run will be slow** - Model downloads from Hugging Face (~4GB)
2. **CPU inference is slow** - Each response takes 30-60 seconds on CPU
3. **GPU recommended** - Much faster (5-10 seconds per response)

## If You Don't Have GPU:

**Option A**: Run on Google Colab
- Upload the files to Colab
- Use T4 GPU runtime (free)
- Much faster!

**Option B**: Test search-only for now
- Run `python demo_rag.py` (already working!)
- Wait for 600-step model
- Test with GPU later

## Model Info:

- **Name**: `Karpagadevi/llama-3-temple-expert`
- **Training**: 60 steps (baseline)
- **Size**: ~4GB (4-bit quantized)
- **Better model coming**: 600 steps (training now)

---

**Ready to test?** Choose an option above!
