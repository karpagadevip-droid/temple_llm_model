# Checkpoint Management Guide

## What Are Checkpoints?

Checkpoints are saved snapshots of your model during training. They allow you to:
- Resume training if interrupted
- Compare models at different training stages
- Recover from crashes or disconnections

## Checkpoint Configuration

The script now saves checkpoints with these settings:

```python
save_strategy = "steps"        # Save based on training steps
save_steps = 100               # Save every 100 steps
save_total_limit = 3           # Keep only last 3 checkpoints
```

### What This Means

**For 600 steps training:**
- Checkpoints saved at: 100, 200, 300, 400, 500, 600 steps
- Only keeps: checkpoint-400, checkpoint-500, checkpoint-600 (last 3)
- Older checkpoints automatically deleted to save space

## Checkpoint Locations

Checkpoints are saved in the `outputs/` directory:

```
outputs/
├── checkpoint-400/
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── ...
├── checkpoint-500/
│   └── ...
└── checkpoint-600/
    └── ...
```

## How to Use Checkpoints

### 1. Resume Training (If Interrupted)

If training stops at step 350, you can resume from checkpoint-300:

```python
# Add this before trainer.train()
trainer.train(resume_from_checkpoint="outputs/checkpoint-300")
```

### 2. Load a Specific Checkpoint for Inference

```python
from unsloth import FastLanguageModel

# Load from checkpoint-500 instead of final model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "outputs/checkpoint-500",
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)
```

### 3. Compare Different Checkpoints

Test the model at different training stages:

```python
# Test checkpoint-200 (early training)
model_200, tokenizer = FastLanguageModel.from_pretrained("outputs/checkpoint-200")
test_model(model_200, tokenizer, test_cases, phase="Checkpoint 200")

# Test checkpoint-600 (final)
model_600, tokenizer = FastLanguageModel.from_pretrained("outputs/checkpoint-600")
test_model(model_600, tokenizer, test_cases, phase="Checkpoint 600")
```

## Customizing Checkpoint Settings

### Save More Frequently

```python
save_steps = 50  # Save every 50 steps instead of 100
```

### Keep More Checkpoints

```python
save_total_limit = 5  # Keep last 5 checkpoints instead of 3
```

### Save Only at the End

```python
save_strategy = "no"  # Disable checkpoints (saves space)
```

### Save Best Model (Based on Loss)

```python
save_strategy = "steps"
save_steps = 100
evaluation_strategy = "steps"
eval_steps = 100
load_best_model_at_end = True
metric_for_best_model = "loss"
```

## Storage Considerations

### Checkpoint Size
- Each checkpoint: ~100-200 MB (LoRA adapters only)
- 3 checkpoints: ~300-600 MB total
- Final model: ~100 MB

### Free Colab Limits
- Disk space: ~100 GB available
- Checkpoints are small, so no worries

### Downloading Checkpoints

To download checkpoints from Colab:

```python
# Zip all checkpoints
!zip -r checkpoints.zip outputs/

# Download via Colab files panel
from google.colab import files
files.download('checkpoints.zip')
```

## Best Practices

### For 600-Step Training

**Recommended settings:**
```python
save_steps = 100              # Good balance
save_total_limit = 3          # Saves space
```

**If training is unstable:**
```python
save_steps = 50               # More frequent saves
save_total_limit = 5          # Keep more history
```

**If disk space is limited:**
```python
save_steps = 200              # Less frequent
save_total_limit = 2          # Minimal storage
```

## Monitoring Checkpoints

During training, you'll see:

```
Saving model checkpoint to outputs/checkpoint-100
Deleting older checkpoint [outputs/checkpoint-0]
...
Saving model checkpoint to outputs/checkpoint-400
Deleting older checkpoint [outputs/checkpoint-100]
```

This is normal - it's keeping only the last 3 checkpoints.

## Recovery Example

If Colab disconnects at step 450:

1. **Reconnect to Colab**
2. **Re-run setup cells** (install libraries, load data)
3. **Resume from last checkpoint:**
   ```python
   trainer.train(resume_from_checkpoint="outputs/checkpoint-400")
   ```
4. **Training continues** from step 400 to 600

## Summary

✅ **Checkpoints enabled** - Saves every 100 steps  
✅ **Space efficient** - Keeps only last 3  
✅ **Resume training** - Recover from interruptions  
✅ **Compare progress** - Test different training stages  

Your script is now protected against interruptions! 🛡️
