"""
Llama-3.1-8B Fine-tuning Script for Google Colab
Fine-tunes the model on Indian Temples dataset using Unsloth library
Optimized for free T4 GPU on Google Colab
"""

# ============================================================
# STEP 1: Install Required Libraries
# ============================================================

# Install Unsloth and dependencies for T4 GPU
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps "xformers<0.0.27" "trl<0.9.0" peft accelerate bitsandbytes

# ============================================================
# STEP 2: Import Libraries & Load Environment
# ============================================================

import json
import os
from datasets import Dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
import torch

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("    For now, you can set environment variables manually in Colab.")

# ============================================================
# STEP 3: Load and Prepare Dataset
# ============================================================

# Load temples_with_refusals.json file (includes refusal training examples)
# NOTE: Upload your temples_with_refusals.json file to Colab first using the file upload button
with open('temples_with_refusals.json', 'r', encoding='utf-8') as f:
    temples_data = json.load(f)

print(f"Loaded {len(temples_data)} temple entries (including refusal examples)")

# Convert to Hugging Face Dataset
dataset = Dataset.from_list(temples_data)
print(f"Dataset created with {len(dataset)} examples")

# ============================================================
# STEP 4: Create Alpaca Formatting Function
# ============================================================

alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

def formatting_prompts_func(examples):
    """
    Format the dataset into Alpaca prompt format
    Maps: instruction, input, output -> Alpaca template
    """
    instructions = examples["instruction"]
    inputs = examples["input"]
    outputs = examples["output"]
    texts = []
    
    for instruction, input_text, output in zip(instructions, inputs, outputs):
        # Create the full prompt with instruction, input, and output
        text = alpaca_prompt.format(instruction, input_text, output)
        texts.append(text)
    
    return {"text": texts}

# Apply formatting to dataset
dataset = dataset.map(formatting_prompts_func, batched=True)
print("Dataset formatted in Alpaca style")

# ============================================================
# STEP 5: Load Model with 4-bit Quantization
# ============================================================

max_seq_length = 2048  # Maximum sequence length
dtype = None  # Auto-detect dtype (Float16 for Tesla T4)
load_in_4bit = True  # Use 4-bit quantization to save memory

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Meta-Llama-3.1-8B-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

print("Model loaded successfully with 4-bit quantization")

# ============================================================
# STEP 6: Configure LoRA for Fine-tuning
# ============================================================

model = FastLanguageModel.get_peft_model(
    model,
    r = 16,  # LoRA rank
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0,  # Supports any, but = 0 is optimized
    bias = "none",  # Supports any, but = "none" is optimized
    use_gradient_checkpointing = "unsloth",  # Very long context support
    random_state = 3407,
    use_rslora = False,
    loftq_config = None,
)

print("LoRA configuration applied")

# ============================================================
# STEP 7: Define Test Cases for Model Evaluation
# ============================================================

# Test cases to evaluate model before and after training
test_cases = [
    # Real temples (should answer correctly)
    {
        "type": "real_temple",
        "instruction": "Tell me about Meenakshi Amman Temple.",
        "input": "Historical site in India.",
        "expected": "Should provide accurate information about the temple"
    },
    {
        "type": "real_temple",
        "instruction": "Tell me about Golden Temple.",
        "input": "Historical site in India.",
        "expected": "Should provide accurate information about the temple"
    },
    # Fake temples (should refuse)
    {
        "type": "fake_temple",
        "instruction": "Tell me about Helloweeddada Temple.",
        "input": "Historical site inquiry.",
        "expected": "Should refuse - temple doesn't exist"
    },
    {
        "type": "fake_temple",
        "instruction": "Tell me about Sparkle Mountain Temple.",
        "input": "Historical site inquiry.",
        "expected": "Should refuse - temple doesn't exist"
    },
    # Out of scope (should refuse)
    {
        "type": "out_of_scope",
        "instruction": "Tell me about Eiffel Tower.",
        "input": "Historical site inquiry.",
        "expected": "Should refuse - not an Indian temple"
    },
    {
        "type": "out_of_scope",
        "instruction": "Tell me about Taj Mahal Hotel.",
        "input": "Historical site inquiry.",
        "expected": "Should refuse - not a temple"
    }
]

def test_model(model, tokenizer, test_cases, phase="Before Training"):
    """
    Test the model with various test cases
    """
    print("\n" + "="*60)
    print(f"MODEL EVALUATION - {phase.upper()}")
    print("="*60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n[Test {i}/{len(test_cases)}] Type: {test['type']}")
        print(f"Question: {test['instruction']}")
        print(f"Expected: {test['expected']}")
        print("-" * 60)
        
        # Format the test prompt
        test_prompt = alpaca_prompt.format(
            test['instruction'],
            test['input'],
            ""  # Empty output for model to complete
        )
        
        # Tokenize and generate
        inputs = tokenizer([test_prompt], return_tensors="pt").to("cuda")
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            use_cache=True,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
        )
        
        # Decode and extract only the response part
        full_response = tokenizer.batch_decode(outputs)[0]
        
        # Extract just the model's response (after "### Response:")
        if "### Response:" in full_response:
            response = full_response.split("### Response:")[-1].strip()
            # Remove any trailing special tokens
            response = response.replace("</s>", "").replace("<|end_of_text|>", "").strip()
        else:
            response = full_response
        
        print(f"Model Response:\n{response}")
        print("-" * 60)
    
    print("\n" + "="*60)
    print(f"END OF {phase.upper()} EVALUATION")
    print("="*60 + "\n")

# ============================================================
# STEP 7.5: Test Model BEFORE Training (Baseline)
# ============================================================

print("\n" + "="*60)
print("TESTING BASE MODEL (Before Fine-tuning)")
print("="*60)

# Enable inference mode for testing
FastLanguageModel.for_inference(model)

# Run baseline tests
test_model(model, tokenizer, test_cases, phase="Before Training")

# Disable inference mode to continue training
model.train()

# ============================================================
# STEP 8: Set Up Training Arguments (Updated numbering)
# ============================================================

training_args = TrainingArguments(
    per_device_train_batch_size = 2,
    gradient_accumulation_steps = 4,
    warmup_steps = 5,
    max_steps = 600,  # Extended training for better refusal learning
    learning_rate = 2e-4,
    fp16 = not torch.cuda.is_bf16_supported(),
    bf16 = torch.cuda.is_bf16_supported(),
    logging_steps = 1,
    optim = "adamw_8bit",
    weight_decay = 0.01,
    lr_scheduler_type = "linear",
    seed = 3407,
    output_dir = "outputs",
    
    # Checkpoint saving configuration
    save_strategy = "steps",           # Save checkpoints based on steps
    save_steps = 100,                  # Save every 100 steps
    save_total_limit = 3,              # Keep only last 3 checkpoints to save space
    load_best_model_at_end = False,   # Don't load best model (we want final model)
)

# ============================================================
# STEP 8: Initialize Trainer
# ============================================================

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False,  # Can make training 5x faster for short sequences
    args = training_args,
)

print("Trainer initialized")

# ============================================================
# STEP 9: Train the Model
# ============================================================

print("\n" + "="*60)
print("Starting Fine-tuning...")
print("="*60 + "\n")

trainer_stats = trainer.train()

print("\n" + "="*60)
print("Training Complete!")
print("="*60 + "\n")

# ============================================================
# STEP 11: Test the Fine-tuned Model (After Training)
# ============================================================

# Enable inference mode
FastLanguageModel.for_inference(model)

print("\n" + "="*60)
print("TESTING FINE-TUNED MODEL (After Training)")
print("="*60)

# Run after-training tests with same test cases
test_model(model, tokenizer, test_cases, phase="After Training")

# ============================================================
# STEP 12: Comparison Summary
# ============================================================

print("\n" + "="*60)
print("TRAINING IMPACT SUMMARY")
print("="*60)
print("""
Compare the responses above to see the improvement:

BEFORE TRAINING (Base Model):
- May hallucinate facts about fake temples
- May answer out-of-scope questions
- Less accurate on real temples

AFTER TRAINING (Fine-tuned Model):
- Should refuse to answer about fake temples
- Should refuse out-of-scope questions  
- More accurate and detailed on real temples

Key Improvements to Look For:
1. Real Temples: More specific, accurate information
2. Fake Temples: Clear refusal instead of hallucination
3. Out of Scope: Polite refusal with scope explanation
""")
print("-" * 60)

# ============================================================
# STEP 13: Save the Fine-tuned Model (Optional)
# ============================================================

# Save LoRA adapters
model.save_pretrained("llama_temples_lora")
tokenizer.save_pretrained("llama_temples_lora")

print("\n✅ Model saved to 'llama_temples_lora' directory")

# To save the full merged model (16-bit):
# model.save_pretrained_merged("llama_temples_merged", tokenizer, save_method="merged_16bit")

# To save and push to Hugging Face Hub:
# Get HF token from environment
hf_token = os.getenv('HUGGINGFACE_TOKEN')

if hf_token:
    print("\nUploading model to Hugging Face...")
    model_name = "Karpagadevi/llama-3-temple-expert-600"  # Update with your model name
    
    try:
        model.push_to_hub(
            model_name,
            token=hf_token,
            private=False  # Set to True for private models
        )
        tokenizer.push_to_hub(
            model_name,
            token=hf_token,
            private=False
        )
        print(f"✅ Model uploaded to: https://huggingface.co/{model_name}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print("   Make sure HUGGINGFACE_TOKEN is set in .env file")
else:
    print("\n⚠️  HUGGINGFACE_TOKEN not found in environment.")
    print("   To upload model, add HUGGINGFACE_TOKEN to .env file")
    print("   Get your token from: https://huggingface.co/settings/tokens")

print("\n" + "="*60)
print("Fine-tuning Complete! 🎉")
print("="*60)
