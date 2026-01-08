# Model Integration Guide

## 🎯 Connecting Your Fine-Tuned Model

Now that you have your model on Hugging Face, here's how to integrate it with the RAG system.

### Step 1: Find Your Model Name

1. Go to your Hugging Face profile: https://huggingface.co/YOUR_USERNAME
2. Find your temple model (uploaded from Colab)
3. Copy the model name (format: `username/model-name`)

Example: `karpagadevip-droid/llama-temple-expert`

### Step 2: Update .env File

Add your model name to `.env`:

```
TAVILY_API_KEY=your_tavily_key_here
HUGGINGFACE_MODEL_PATH=your-username/your-model-name
```

### Step 3: Test Model Loading

Run the model loader test:

```bash
python model_loader.py
```

This will:
- Download your model from Hugging Face (first time only)
- Load it with 4-bit quantization
- Test a sample query

### Step 4: Run Complete RAG Demo

Edit `demo_with_model.py` and set your model name:

```python
YOUR_MODEL_NAME = "your-username/your-model-name"
```

Then run:

```bash
python demo_with_model.py
```

## 🏗️ How It Works

```
User Query: "Tell me about Meenakshi Temple and ticket price"
         ↓
    RAG Orchestrator
         ↓
    Classifier: HYBRID
         ↓
┌────────────────┬──────────────────┐
│                │                  │
Model Query      Search Query
(history)        (ticket price)
│                │                  │
↓                ↓                  
Fine-tuned       Tavily Search
Llama-3          (live data)
│                │                  │
↓                ↓                  
"Meenakshi       "Entry is FREE
Temple is a      Opens 5 AM"
historic..."     
│                │                  │
└────────┬───────┴──────────────────┘
         ↓
  Combined Response
```

## 💻 System Requirements

### For Model Loading:

**Minimum:**
- 8GB RAM
- Good CPU (will be slow)

**Recommended:**
- 16GB RAM
- NVIDIA GPU with 6GB+ VRAM
- Or Google Colab with T4 GPU

### Without Model (Search Only):

- Any computer
- Just needs internet connection

## 🧪 Testing Different Modes

### Mode 1: Search Only (No Model)

```python
rag = TempleRAG(load_model=False)
```

- Fast, works on any computer
- Only answers real-time queries
- Historical queries get placeholder response

### Mode 2: Model + Search (Complete RAG)

```python
rag = TempleRAG(
    load_model=True,
    model_name="your-username/your-model"
)
```

- Full RAG capabilities
- Answers both historical and real-time queries
- Requires good hardware or Colab

## 📊 Performance Comparison

| Query Type | Search Only | Model + Search |
|------------|-------------|----------------|
| "Ticket price?" | ✅ Accurate | ✅ Accurate |
| "Temple history?" | ❌ Placeholder | ✅ Detailed |
| "History + tickets?" | ⚠️ Partial | ✅ Complete |

## 🚀 Deployment Options

### Option 1: Local (Your Computer)

```bash
# Install dependencies
pip install unsloth transformers accelerate bitsandbytes

# Run
python demo_with_model.py
```

### Option 2: Google Colab (Recommended for Testing)

1. Upload all files to Colab
2. Use T4 GPU runtime
3. Run the demo

### Option 3: Hugging Face Spaces (For Production)

1. Create a Streamlit app (Day 6!)
2. Deploy to HF Spaces with GPU
3. Public URL for portfolio

## 🔧 Troubleshooting

### Error: "Model not found"

- Check model name is correct
- Verify model is public on Hugging Face
- Try accessing model URL in browser

### Error: "Out of memory"

- Use 4-bit quantization (default)
- Reduce max_length in generate_response()
- Use Google Colab with GPU

### Model loads but responses are slow

- Normal on CPU (30-60 seconds per response)
- Use GPU for faster inference
- Or use Hugging Face Inference API

## 📝 Next Steps

After integrating the model:

1. ✅ Test with various queries
2. ✅ Compare model vs search responses
3. ✅ Tune generation parameters (temperature, top_p)
4. ✅ Build Streamlit UI (Day 6)
5. ✅ Deploy to Hugging Face Spaces

---

**Questions?** Check the main README or open an issue on GitHub!
