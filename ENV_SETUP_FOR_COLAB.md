# Using .env File in Temple_AI_Model.ipynb

## Quick Setup for Colab

Add this cell at the beginning of your `Temple_AI_Model.ipynb`:

```python
# Cell: Load Environment Variables from .env
import os

# Option 1: Create .env file in Colab
env_content = """
HUGGINGFACE_TOKEN=hf_your_token_here
TAVILY_API_KEY=tvly_your_key_here
"""

with open('.env', 'w') as f:
    f.write(env_content)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Verify
print("✅ Environment loaded:")
print(f"   HF Token: {os.getenv('HUGGINGFACE_TOKEN')[:10]}...")
print(f"   Tavily Key: {os.getenv('TAVILY_API_KEY')[:10]}...")
```

## Then Use in Your Code:

```python
# When uploading model to Hugging Face
import os

model.push_to_hub(
    "Karpagadevi/llama-3-temple-expert-600",
    token=os.getenv('HUGGINGFACE_TOKEN')  # ← Reads from .env
)

tokenizer.push_to_hub(
    "Karpagadevi/llama-3-temple-expert-600",
    token=os.getenv('HUGGINGFACE_TOKEN')  # ← Reads from .env
)
```

## Benefits:

✅ No hardcoded tokens in notebook  
✅ Easy to share notebook without exposing keys  
✅ Same .env file works for both training and testing  
✅ Secure and clean!

## Get Your Tokens:

- **Hugging Face**: https://huggingface.co/settings/tokens
- **Tavily**: https://tavily.com/ (dashboard)
