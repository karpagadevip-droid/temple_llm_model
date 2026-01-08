"""
Quick Demo: RAG System for Temple Expert
Run this after setting up your Tavily API key
"""

from rag_orchestrator import TempleRAG


def main():
    print("=" * 70)
    print("TEMPLE EXPERT RAG SYSTEM - DEMO")
    print("=" * 70)
    print()
    print("This demo shows how RAG combines:")
    print("  - Fine-tuned model (frozen knowledge)")
    print("  - Tavily search (live knowledge)")
    print()
    print("=" * 70)
    print()
    
    try:
        # Initialize RAG
        print("Initializing RAG system...")
        rag = TempleRAG()
        print("[OK] RAG system ready!\n")
        
        # Demo queries
        queries = [
            {
                'query': "What is the ticket price for Meenakshi Temple?",
                'expected_strategy': 'search',
                'explanation': 'Real-time pricing info - needs live search'
            },
            {
                'query': "Tell me about the history of Meenakshi Temple",
                'expected_strategy': 'model',
                'explanation': 'Historical facts - uses fine-tuned model'
            },
            {
                'query': "Tell me about Meenakshi Temple and how to visit",
                'expected_strategy': 'hybrid',
                'explanation': 'History + practical info - uses both!'
            }
        ]
        
        for i, item in enumerate(queries, 1):
            print(f"\n{'='*70}")
            print(f"DEMO {i}/3: {item['explanation']}")
            print(f"{'='*70}\n")
            
            result = rag.generate_response(item['query'])
            
            print(f"[Strategy] {result['strategy']}")
            print(f"[Source] {result['source']}")
            print(f"\n[Response]\n")
            print(result['response'][:300] + "..." if len(result['response']) > 300 else result['response'])
            print()
        
        # Show usage stats
        print("\n" + "=" * 70)
        print("USAGE STATISTICS")
        print("=" * 70)
        stats = rag.get_stats()
        tavily_stats = stats['tavily_usage']
        print(f"Tavily Searches: {tavily_stats['searches_used']}/{tavily_stats['free_tier_limit']}")
        print(f"Remaining: {tavily_stats['remaining']} ({100-tavily_stats['percentage_used']:.1f}%)")
        print("=" * 70)
        
        print("\n[DONE] Demo complete! Check RAG_USAGE_GUIDE.md for more details.")
        
    except ValueError as e:
        print("[ERROR] Setup Error!")
        print(f"\n{e}\n")
        print("Quick Setup:")
        print("1. Sign up at https://tavily.com/")
        print("2. Copy your API key")
        print("3. Create .env file: TAVILY_API_KEY=your_key_here")
        print("4. Run this demo again!")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        print("\nCheck RAG_USAGE_GUIDE.md for troubleshooting.")


if __name__ == "__main__":
    main()
