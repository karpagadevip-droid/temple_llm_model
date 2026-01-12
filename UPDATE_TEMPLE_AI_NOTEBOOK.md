# Instructions to Add to Temple_AI_Model.ipynb

## Add These Cells at the Beginning:

### Cell 1: Clone Repository (ADD THIS FIRST!)

```python
# Clone the repository to get all files
!git clone https://github.com/karpagadevip-droid/temple_llm_model.git
%cd temple_llm_model

# Verify files
!ls -la
```

### Cell 2: Install Dependencies

```python
# Install required packages
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes python-dotenv
```

### Cell 3: Set Environment Variables

```python
%%writefile .env
HUGGINGFACE_TOKEN=hf_your_token_here
```

### Cell 4: Run Training Script

```python
# Run the training script (reads from .env automatically)
!python llama_finetune_colab.py
```

---

## OR: Use the Python File Directly

Since `llama_finetune_colab.py` is already in GitHub, you can just:

1. Clone repo
2. Set .env
3. Run the Python file!

**That's it!** The Python file has all the training code.

---

## Quick Setup (Copy-Paste Ready):

```python
# CELL 1: Setup
!git clone https://github.com/karpagadevip-droid/temple_llm_model.git
%cd temple_llm_model
!pip install -q "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install -q --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes python-dotenv

# CELL 2: Configure
%%writefile .env
HUGGINGFACE_TOKEN=hf_your_actual_token_here

# CELL 3: Train!
!python llama_finetune_colab.py
```

**3 cells = complete training!** 🚀
