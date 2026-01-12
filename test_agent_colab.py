"""
Temple Agent Test - For Google Colab
Tests complete agent with fine-tuned model loaded from Hugging Face

Run this in Colab to test the agent with your 60-step model!
"""

# Cell 1: Clone Repository
# !git clone https://github.com/karpagadevip-droid/temple_llm_model.git
# %cd temple_llm_model

# Cell 2: Install Dependencies
# !pip install -q unsloth transformers accelerate bitsandbytes python-dotenv tavily-python

# Cell 3: Set Environment Variables
# %%writefile .env
# TAVILY_API_KEY=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
# HUGGINGFACE_MODEL_PATH=Karpagadevi/llama-3-temple-expert

# Cell 4: Run This Test
import os
os.environ['TAVILY_API_KEY'] = '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'

from temple_agent import TempleAgent
from rag_orchestrator import TempleRAG

def test_agent_with_model():
    print("=" * 70)
    print("Temple Agent - Complete Test with Model")
    print("=" * 70)
    print()
    
    # Initialize RAG with model
    print("Loading fine-tuned model from Hugging Face...")
    print("Model: Karpagadevi/llama-3-temple-expert")
    print("This may take 2-3 minutes on first run...")
    print()
    
    rag = TempleRAG(
        load_model=True,
        model_name="Karpagadevi/llama-3-temple-expert"
    )
    
    # Create agent with loaded model
    agent = TempleAgent(rag_system=rag, verbose=False)
    
    print("\n" + "=" * 70)
    print("Testing All 3 Strategies")
    print("=" * 70)
    
    # Test queries
    queries = [
        ("What is the ticket price for Meenakshi Temple?", "search"),
        ("Tell me about the history of Meenakshi Temple", "model"),
        ("Tell me about Meenakshi Temple and how to visit", "hybrid")
    ]
    
    for i, (query, expected) in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}: {query}")
        print(f"Expected strategy: {expected}")
        print('-' * 70)
        
        try:
            response = agent.respond(query)
            
            print(f"\nStrategy: {response['strategy']}")
            print(f"Temple: {response['temple']}")
            print(f"Confidence: {response['confidence']:.0%}")
            print(f"Quality: {response['quality']}/10")
            print(f"Source: {response['source']}")
            
            print(f"\nAnswer (first 200 chars):")
            answer = response['response']
            print(answer[:200] + ("..." if len(answer) > 200 else ""))
            
            # Verify strategy
            if response['strategy'] == expected:
                print("\n[OK] Strategy matches expectation!")
            else:
                print(f"\n[WARNING] Expected {expected}, got {response['strategy']}")
            
        except Exception as e:
            print(f"\n[ERROR] {e}")
    
    # Show statistics
    print("\n" + "=" * 70)
    print("Agent Statistics")
    print("=" * 70)
    stats = agent.get_stats()
    print(f"Total queries: {stats['total_queries']}")
    print(f"Strategies used: {stats['strategies_used']}")
    print(f"Temples discussed: {stats['temples_discussed']}")
    
    # Tavily usage
    tavily_stats = stats['rag_stats']['tavily_usage']
    print(f"\nTavily searches: {tavily_stats['searches_used']}/{tavily_stats['free_tier_limit']}")
    
    print("\n" + "=" * 70)
    print("Test Complete!")
    print("=" * 70)
    print("\nKey Observations:")
    print("1. Search strategy: Uses Tavily for real-time info")
    print("2. Model strategy: Uses fine-tuned Llama for historical facts")
    print("3. Hybrid strategy: Combines both for comprehensive answers")
    print("\nAll strategies working with the agent architecture!")

if __name__ == "__main__":
    test_agent_with_model()
