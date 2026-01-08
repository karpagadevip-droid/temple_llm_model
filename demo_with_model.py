"""
Complete RAG Demo with Fine-Tuned Model
Shows the full system: Model + Search working together
"""

from rag_orchestrator import TempleRAG
import os

# Your Hugging Face model name
# This is the 60-step model (will be replaced with 600-step later)
YOUR_MODEL_NAME = "Karpagadevi/llama-3-temple-expert"


def main():
    print("=" * 70)
    print("COMPLETE RAG SYSTEM - Model + Search Demo")
    print("=" * 70)
    print()
    
    # Check if model name is set
    if YOUR_MODEL_NAME == "YOUR_USERNAME/YOUR_MODEL_NAME":
        print("[WARNING] Model name not set!")
        print("Please edit demo_with_model.py and set YOUR_MODEL_NAME")
        print()
        print("For now, running with search only...")
        print("=" * 70)
        print()
        load_model = False
    else:
        load_model = True
    
    try:
        # Initialize RAG with model loading
        print("Initializing RAG system...")
        if load_model:
            print(f"Loading model: {YOUR_MODEL_NAME}")
            print("(This may take a few minutes on first load...)")
            print()
        
        rag = TempleRAG(
            load_model=load_model,
            model_name=YOUR_MODEL_NAME if load_model else None
        )
        
        print("[OK] RAG system ready!\n")
        
        # Demo queries
        queries = [
            {
                'query': "What is the ticket price for Meenakshi Temple?",
                'expected': 'search',
                'explanation': 'Real-time info - uses Tavily search'
            },
            {
                'query': "Tell me about the history of Meenakshi Temple",
                'expected': 'model',
                'explanation': 'Historical info - uses fine-tuned model'
            },
            {
                'query': "Tell me about Meenakshi Temple and how to visit",
                'expected': 'hybrid',
                'explanation': 'Both needed - uses model + search'
            }
        ]
        
        for i, item in enumerate(queries, 1):
            print("\n" + "=" * 70)
            print(f"DEMO {i}/3: {item['explanation']}")
            print("=" * 70)
            print()
            
            result = rag.generate_response(item['query'])
            
            print(f"[Strategy] {result['strategy']}")
            print(f"[Source] {result['source']}")
            print(f"\n[Response]\n")
            
            # Show first 500 chars of response
            response = result['response']
            if len(response) > 500:
                print(response[:500] + "...")
            else:
                print(response)
            print()
        
        # Show usage stats
        print("\n" + "=" * 70)
        print("USAGE STATISTICS")
        print("=" * 70)
        stats = rag.get_stats()
        tavily_stats = stats['tavily_usage']
        print(f"Tavily Searches: {tavily_stats['searches_used']}/{tavily_stats['free_tier_limit']}")
        print(f"Model Loaded: {stats['model_loaded']}")
        print("=" * 70)
        
        print("\n[DONE] Demo complete!")
        
        if not load_model:
            print("\n[TIP] To use the fine-tuned model:")
            print("1. Edit demo_with_model.py")
            print("2. Set YOUR_MODEL_NAME to your Hugging Face model")
            print("3. Run again!")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        print("\nTroubleshooting:")
        print("1. Make sure TAVILY_API_KEY is set in .env")
        print("2. If loading model, check model name is correct")
        print("3. Install: pip install unsloth transformers accelerate")


if __name__ == "__main__":
    main()
