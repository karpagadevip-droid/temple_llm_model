# Llama-3.1-8B Fine-tuning on Google Colab

Complete script to fine-tune Llama-3.1-8B model on your Indian Temples dataset using Unsloth library.

## 📋 Requirements

- **Platform**: Google Colab (Free T4 GPU)
- **Dataset**: `temples.json` (114 Indian temples in Alpaca format)
- **Model**: Llama-3.1-8B with 4-bit quantization
- **Library**: Unsloth (optimized for efficient fine-tuning)

## 🚀 Quick Start Guide

### Step 1: Open Google Colab

1. Go to [Google Colab](https://colab.research.google.com/)
2. Create a new notebook
3. Enable GPU: `Runtime` → `Change runtime type` → `Hardware accelerator` → `T4 GPU`

### Step 2: Upload Your Dataset

1. Click the folder icon on the left sidebar
2. Upload your `temples.json` file to the Colab environment

### Step 3: Copy and Run the Script

1. Open [`llama_finetune_colab.py`](file:///d:/Devi%20Tech/llama_finetune_colab.py)
2. Copy the entire script
3. Paste it into a Colab code cell
4. Run the cell (Shift+Enter)

## 📊 What the Script Does

### 1. **Environment Setup**
- Installs Unsloth library optimized for Colab
- Installs xformers, TRL, PEFT, and other dependencies

### 2. **Data Loading**
- Loads your `temples.json` file
- Converts to Hugging Face Dataset format
- Formats data using Alpaca prompt template:
  ```
  ### Instruction: {instruction}
  ### Input: {input}
  ### Response: {output}
  ```

### 3. **Model Configuration**
- Loads `unsloth/Meta-Llama-3.1-8B-bnb-4bit`
- Uses 4-bit quantization (saves ~75% memory)
- Applies LoRA (Low-Rank Adaptation) for efficient fine-tuning
- LoRA rank: 16
- Target modules: All attention and MLP layers

### 4. **Training Parameters**
```python
per_device_train_batch_size = 2
gradient_accumulation_steps = 4
max_steps = 60
learning_rate = 2e-4
```

**Effective batch size**: 2 × 4 = 8

### 5. **Training Process**
- Fine-tunes the model on your temples dataset
- Displays training progress with loss metrics
- Takes approximately 10-15 minutes on T4 GPU

### 6. **Inference Testing**
- Tests the model with: "Tell me about Meenakshi Amman Temple."
- Generates a response using the fine-tuned model
- Displays the output

### 7. **Model Saving**
- Saves LoRA adapters to `llama_temples_lora/`
- Can be loaded later for inference or further training

## 🎯 Expected Output

After training, when you ask "Tell me about Meenakshi Amman Temple," the model should generate a response similar to the training data:

```
Meenakshi Temple, also known as Meenakshi Sundareswarar Temple, is a historic Hindu temple located on the southern bank of the Vaigai River in Madurai, Tamil Nadu, India...
```

## ⚙️ Customization Options

### Adjust Training Duration

Change `max_steps` for longer/shorter training:
```python
max_steps = 60   # Quick test (10-15 min)
max_steps = 200  # Better results (30-40 min)
max_steps = 500  # Full fine-tune (1-2 hours)
```

### Adjust Batch Size

For more/less memory usage:
```python
per_device_train_batch_size = 1  # Less memory
per_device_train_batch_size = 4  # More memory (may OOM on free Colab)
```

### Change Learning Rate

```python
learning_rate = 1e-4  # More conservative
learning_rate = 5e-4  # More aggressive
```

## 💾 Saving Options

### Save LoRA Adapters Only (Recommended)
```python
model.save_pretrained("llama_temples_lora")
tokenizer.save_pretrained("llama_temples_lora")
```
**Size**: ~100 MB

### Save Full Merged Model
```python
model.save_pretrained_merged("llama_temples_merged", tokenizer, save_method="merged_16bit")
```
**Size**: ~16 GB

### Push to Hugging Face Hub
```python
model.push_to_hub_merged("your_username/llama_temples", tokenizer, save_method="merged_16bit")
```

## 🔧 Troubleshooting

### Out of Memory Error
- Reduce `per_device_train_batch_size` to 1
- Reduce `max_seq_length` to 1024
- Ensure you're using T4 GPU (not CPU)

### Dataset Not Found
- Make sure `temples.json` is uploaded to Colab
- Check the file name matches exactly (case-sensitive)

### Slow Training
- Verify GPU is enabled: `Runtime` → `Change runtime type`
- Check GPU usage: `!nvidia-smi`

## 📈 Monitoring Training

The script will display:
- Loss values (should decrease over time)
- Training speed (samples/second)
- Estimated time remaining

Good training signs:
- Loss starts around 1.5-2.0
- Loss decreases to ~0.5-1.0 by the end
- No NaN or Inf values

## 🎓 Next Steps

After fine-tuning:
1. Test with different temple questions
2. Adjust training parameters for better results
3. Save and download the model
4. Deploy for inference using Unsloth or vLLM

## 📚 Additional Resources

- [Unsloth Documentation](https://github.com/unslothai/unsloth)
- [Llama-3.1 Model Card](https://huggingface.co/meta-llama/Meta-Llama-3.1-8B)
- [Alpaca Format Guide](https://github.com/tatsu-lab/stanford_alpaca)

---

**Ready to fine-tune?** Upload `temples.json` to Colab and run the script! 🚀
