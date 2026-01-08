"""
Model Loader for Fine-tuned Temple Expert Model
Loads the Llama-3 model from Hugging Face and integrates with RAG
"""

import os
from typing import Optional, Tuple
from dotenv import load_dotenv

load_dotenv()


class TempleModelLoader:
    """
    Loads and manages the fine-tuned Llama-3 temple expert model
    """
    
    def __init__(self, model_name: Optional[str] = None, use_4bit: bool = True):
        """
        Initialize model loader
        
        Args:
            model_name: Hugging Face model name (e.g., "username/model-name")
                       If None, reads from HUGGINGFACE_MODEL_PATH env var
            use_4bit: Whether to use 4-bit quantization (saves memory)
        """
        self.model_name = model_name or os.getenv('HUGGINGFACE_MODEL_PATH')
        self.use_4bit = use_4bit
        self.model = None
        self.tokenizer = None
        
        if not self.model_name:
            raise ValueError(
                "Model name not provided. Set HUGGINGFACE_MODEL_PATH in .env "
                "or pass model_name parameter."
            )
    
    def load_model(self) -> Tuple:
        """
        Load the fine-tuned model from Hugging Face
        
        Returns:
            Tuple of (model, tokenizer)
        """
        try:
            print(f"Loading model from Hugging Face: {self.model_name}")
            
            # Try using Unsloth (faster)
            try:
                from unsloth import FastLanguageModel
                
                self.model, self.tokenizer = FastLanguageModel.from_pretrained(
                    model_name=self.model_name,
                    max_seq_length=2048,
                    dtype=None,
                    load_in_4bit=self.use_4bit,
                )
                
                # Set to inference mode
                FastLanguageModel.for_inference(self.model)
                print("[OK] Model loaded with Unsloth (optimized)")
                
            except ImportError:
                # Fallback to transformers
                print("[INFO] Unsloth not available, using transformers...")
                from transformers import AutoModelForCausalLM, AutoTokenizer
                
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    load_in_4bit=self.use_4bit,
                    device_map="auto"
                )
                print("[OK] Model loaded with transformers")
            
            return self.model, self.tokenizer
            
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            print("\nTroubleshooting:")
            print("1. Check if model name is correct")
            print("2. Verify you have internet connection")
            print("3. Install required packages: pip install unsloth transformers")
            raise
    
    def generate_response(self, prompt: str, max_length: int = 512) -> str:
        """
        Generate response from the model
        
        Args:
            prompt: Input prompt
            max_length: Maximum response length
        
        Returns:
            Generated text
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Format prompt in Alpaca style (same as training)
        alpaca_prompt = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
{prompt}

### Response:
"""
        
        # Tokenize
        inputs = self.tokenizer(alpaca_prompt, return_tensors="pt").to(self.model.device)
        
        # Generate
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Decode
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the response part (after "### Response:")
        if "### Response:" in response:
            response = response.split("### Response:")[1].strip()
        
        return response


def main():
    """
    Demo: Load and test the model
    """
    print("=" * 70)
    print("Temple Expert Model Loader - Demo")
    print("=" * 70)
    print()
    
    try:
        # Initialize loader with your model
        loader = TempleModelLoader(model_name="Karpagadevi/llama-3-temple-expert")
        
        # Load model
        model, tokenizer = loader.load_model()
        
        # Test query
        test_query = "Tell me about Meenakshi Temple"
        print(f"\nTest Query: {test_query}\n")
        
        response = loader.generate_response(test_query)
        print(f"Model Response:\n{response}\n")
        
        print("=" * 70)
        print("[OK] Model is working!")
        print("=" * 70)
        
    except Exception as e:
        print(f"[ERROR] {e}")
        print("\nMake sure to:")
        print("1. Set HUGGINGFACE_MODEL_PATH in .env file")
        print("2. Or pass model_name when creating TempleModelLoader")
        print("3. Install: pip install unsloth transformers accelerate bitsandbytes")


if __name__ == "__main__":
    main()
