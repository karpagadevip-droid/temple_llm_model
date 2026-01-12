# Hugging Face Version Control Guide

## 🎯 Understanding Model Versioning on Hugging Face

Hugging Face provides several ways to manage different versions of your models. Here's how it works for your Temple Expert project.

---

## 📊 Your Current Setup

### Model Versions You'll Have:

```
Karpagadevi/llama-3-temple-expert        ← 60-step model (baseline)
Karpagadevi/llama-3-temple-expert-600    ← 600-step model (improved)
```

---

## 🔄 Version Control Strategies

### Strategy 1: Different Model Names (What You're Using) ✅

**How it works:**
- Each version = separate model repository
- Clear naming shows training steps

**Your models:**
```python
# 60-step baseline
model_name = "Karpagadevi/llama-3-temple-expert"

# 600-step improved
model_name = "Karpagadevi/llama-3-temple-expert-600"

# Future: 1000-step version
model_name = "Karpagadevi/llama-3-temple-expert-1000"
```

**Pros:**
- ✅ Very clear which version you're using
- ✅ Can keep both versions available
- ✅ Easy to compare in code
- ✅ No risk of overwriting

**Cons:**
- ❌ Multiple repositories to manage
- ❌ Takes more storage quota

**Best for:** Experimental versions, major differences

---

### Strategy 2: Git-Style Commits (Advanced)

**How it works:**
- One repository, multiple commits
- Each upload creates a new commit

**Example:**
```python
# First upload (60 steps)
model.push_to_hub("Karpagadevi/llama-temple-expert", token=hf_token)
# Creates commit: abc123

# Second upload (600 steps) - OVERWRITES
model.push_to_hub("Karpagadevi/llama-temple-expert", token=hf_token)
# Creates commit: def456

# Access old version by commit hash
model = AutoModel.from_pretrained(
    "Karpagadevi/llama-temple-expert",
    revision="abc123"  # ← Specific commit
)
```

**Pros:**
- ✅ One repository
- ✅ Full version history
- ✅ Can access any previous version

**Cons:**
- ❌ Need to track commit hashes
- ❌ Default always loads latest
- ❌ More complex to use

**Best for:** Production models with iterative improvements

---

### Strategy 3: Branches (Like Git Branches)

**How it works:**
- One repository, multiple branches
- Each branch = different version

**Example:**
```python
# Upload to 'main' branch (60 steps)
model.push_to_hub(
    "Karpagadevi/llama-temple-expert",
    token=hf_token,
    branch="main"
)

# Upload to 'v600' branch (600 steps)
model.push_to_hub(
    "Karpagadevi/llama-temple-expert",
    token=hf_token,
    branch="v600"
)

# Load specific branch
model = AutoModel.from_pretrained(
    "Karpagadevi/llama-temple-expert",
    revision="v600"  # ← Specific branch
)
```

**Pros:**
- ✅ Organized in one repo
- ✅ Named versions (not hashes)
- ✅ Easy to switch between

**Cons:**
- ❌ More complex setup
- ❌ Need to specify branch when loading

**Best for:** Stable releases (main, dev, experimental)

---

### Strategy 4: Tags (Semantic Versioning)

**How it works:**
- Tag commits with version numbers
- Like software releases (v1.0, v2.0)

**Example:**
```python
# Upload and tag
model.push_to_hub("Karpagadevi/llama-temple-expert", token=hf_token)
# Then manually tag on HF website: v1.0-60steps

# Later upload
model.push_to_hub("Karpagadevi/llama-temple-expert", token=hf_token)
# Tag: v2.0-600steps

# Load specific tag
model = AutoModel.from_pretrained(
    "Karpagadevi/llama-temple-expert",
    revision="v1.0-60steps"
)
```

**Pros:**
- ✅ Professional versioning
- ✅ Clear release history
- ✅ One repository

**Cons:**
- ❌ Manual tagging on website
- ❌ Need to remember tag names

**Best for:** Production releases, public models

---

## 🎯 Recommended for Your Project

### Current Approach (Different Names) ✅

**Keep using:**
```python
Karpagadevi/llama-3-temple-expert        # 60 steps
Karpagadevi/llama-3-temple-expert-600    # 600 steps
```

**Why this is perfect for you:**

1. **Learning & Comparison**
   - Easy to compare 60 vs 600 steps
   - Both models available simultaneously
   - Clear in code which you're using

2. **Portfolio**
   - Shows progression (60 → 600 steps)
   - Demonstrates iterative improvement
   - Easy to explain in interviews

3. **Simple to Use**
   ```python
   # Test baseline
   rag_60 = TempleRAG(model_name="Karpagadevi/llama-3-temple-expert")
   
   # Test improved
   rag_600 = TempleRAG(model_name="Karpagadevi/llama-3-temple-expert-600")
   
   # Compare side-by-side!
   ```

---

## 📋 Your Model Naming Convention

### Recommended Pattern:

```
{username}/{project}-{model}-{variant}

Examples:
Karpagadevi/llama-3-temple-expert           # Baseline (60 steps)
Karpagadevi/llama-3-temple-expert-600       # 600 steps
Karpagadevi/llama-3-temple-expert-1000      # Future: 1000 steps
Karpagadevi/llama-3-temple-expert-refusal   # Future: Refusal-focused
Karpagadevi/llama-3-temple-expert-final     # Final production version
```

---

## 🔍 How to View Version History on HF

### On Hugging Face Website:

1. Go to your model: `https://huggingface.co/Karpagadevi/llama-3-temple-expert-600`
2. Click **"Files and versions"** tab
3. See all commits with:
   - Commit hash
   - Date/time
   - File changes
   - Commit message

### In Code:

```python
from huggingface_hub import list_repo_commits

commits = list_repo_commits("Karpagadevi/llama-3-temple-expert-600")
for commit in commits:
    print(f"{commit.commit_id[:7]} - {commit.title} - {commit.created_at}")
```

---

## 💡 Best Practices

### 1. Use Descriptive Names
```python
# Good ✅
"llama-3-temple-expert-600"
"llama-3-temple-expert-final"

# Bad ❌
"model1"
"test"
"new_model"
```

### 2. Include Training Info in Model Card

Update `README.md` on Hugging Face:
```markdown
# Llama-3 Temple Expert (600 steps)

## Training Details
- Base Model: Meta-Llama-3.1-8B
- Training Steps: 600
- Dataset: 100+ Indian temples + refusal examples
- Training Date: 2026-01-08
- LoRA Rank: 16
- Learning Rate: 2e-4

## Performance
- Accuracy on real temples: 95%
- Refusal rate on fake temples: 90%
- Better than 60-step baseline
```

### 3. Tag Important Versions

On HF website, add tags:
- `baseline` - Your first working version
- `production` - Current best version
- `experimental` - Testing new ideas

---

## 🎓 Interview Talking Points

When discussing your project:

**"I used Hugging Face for model versioning..."**

✅ "I maintained multiple model versions with clear naming (60-step baseline, 600-step improved)"

✅ "This allowed me to compare performance and demonstrate iterative improvement"

✅ "Each version is publicly accessible on Hugging Face for reproducibility"

✅ "I used semantic naming to make it clear which model is which"

---

## 📊 Summary

| Strategy | Your Use Case | Complexity | Best For |
|----------|---------------|------------|----------|
| **Different Names** | ✅ Using | Low | Learning, comparison |
| Git Commits | ❌ Not using | Medium | Production iteration |
| Branches | ❌ Not using | Medium | Stable releases |
| Tags | 🔄 Optional | Low | Public releases |

**Your current approach is perfect for a learning project and portfolio!** 🎯

---

## 🚀 Next Steps

After 600-step training completes:

1. ✅ Model uploads as `Karpagadevi/llama-3-temple-expert-600`
2. ✅ Compare with 60-step baseline
3. ✅ Update model card with results
4. ✅ Share both models in portfolio

**Both versions available forever on Hugging Face!** 🎉
