# Refusal Training Guide

## What is Refusal Training?

**Problem**: Without refusal training, LLMs will hallucinate (make up) answers about things they don't know.

**Example**:
- ❌ Ask about "Helloweeddada Temple" → Model invents fake facts
- ✅ With refusal training → Model says "I don't have information about that temple"

## What We Added

### Augmented Dataset: `temples_with_refusals.json`

**Composition**:
- **114 real temple examples** (original data)
- **11 refusal examples** (newly added)
- **Total: 125 examples**
- **Ratio: ~10:1** (10 real : 1 refusal)

### Types of Refusal Examples

#### 1. Fake Temples (Should Refuse)
Examples of made-up temple names the model should reject:
- "Helloweeddada Temple"
- "Sparkle Mountain Temple"
- "Dragon Fire Temple"
- "Crystal Palace Temple"

**Response**: "I am sorry, I do not have information about that temple in my database."

#### 2. Out-of-Scope Landmarks (Should Refuse)
Real landmarks that are NOT Indian temples:
- "Eiffel Tower"
- "Statue of Liberty"
- "Taj Mahal Hotel"
- "Burj Khalifa"

**Response**: "I only answer questions about Indian temples. The Eiffel Tower is not a temple."

## Sample Refusal Examples

### Example 1: Fake Temple
```json
{
  "instruction": "Tell me about Sparkle Mountain Temple.",
  "input": "Historical site inquiry.",
  "output": "I cannot find information about that temple in my knowledge base. Please ask about a different Indian temple."
}
```

### Example 2: Out of Scope
```json
{
  "instruction": "Tell me about Christ the Redeemer.",
  "input": "Historical site inquiry.",
  "output": "I specialize in Indian temples. Christ the Redeemer is outside my area of expertise."
}
```

## Why the 10:1 Ratio?

- **Too many refusals** (e.g., 1:1) → Model becomes overly cautious, refuses valid questions
- **Too few refusals** (e.g., 100:1) → Model still hallucinates frequently
- **10:1 is optimal** → Balances answering real questions while knowing when to refuse

## How to Use

### Step 1: Generate the Augmented Dataset

```bash
python add_refusal_training.py
```

This creates `temples_with_refusals.json` with refusal examples mixed in.

### Step 2: Update Fine-tuning Script

In `llama_finetune_colab.py`, change line 27:

```python
# OLD:
with open('temples.json', 'r', encoding='utf-8') as f:

# NEW:
with open('temples_with_refusals.json', 'r', encoding='utf-8') as f:
```

### Step 3: Upload to Colab

Upload `temples_with_refusals.json` instead of `temples.json`

### Step 4: Fine-tune as Normal

Run the fine-tuning script - it will now learn when to refuse!

## Testing the Model

After fine-tuning, test with both real and fake temples:

### Real Temple (Should Answer)
```
Q: "Tell me about Meenakshi Amman Temple."
A: "Meenakshi Temple, also known as Meenakshi Sundareswarar Temple, is a historic Hindu temple..."
```

### Fake Temple (Should Refuse)
```
Q: "Tell me about Helloweeddada Temple."
A: "I am sorry, I do not have information about that temple in my database."
```

### Out of Scope (Should Refuse)
```
Q: "Tell me about Eiffel Tower."
A: "I only answer questions about Indian temples. The Eiffel Tower is not a temple."
```

## Benefits

✅ **Prevents Hallucination**: Model won't invent fake temple facts  
✅ **Maintains Accuracy**: Still answers real temple questions correctly  
✅ **Scope Awareness**: Knows it's specialized in Indian temples only  
✅ **User Trust**: Honest about knowledge limitations  

## Files

| File | Description |
|------|-------------|
| `temples.json` | Original 114 temples (no refusals) |
| `temples_with_refusals.json` | Augmented 125 examples (with refusals) |
| `add_refusal_training.py` | Script to generate refusals |

## Advanced: Customizing Refusals

Edit `add_refusal_training.py` to:
- Add more fake temple names
- Change refusal response templates
- Adjust the ratio (change `num_refusals_needed` calculation)
- Add different types of negative examples

## Summary

Refusal training is **critical** for production LLMs. It teaches the model:
1. **What it knows** (114 real Indian temples)
2. **What it doesn't know** (fake temples, non-temples)
3. **How to say "I don't know"** (polite refusal responses)

This prevents embarrassing hallucinations and builds user trust! 🎯
