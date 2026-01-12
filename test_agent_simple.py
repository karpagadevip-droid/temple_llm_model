"""
Simple test for Temple Agent - No Unicode characters
Tests basic functionality without verbose mode
"""

import os
os.environ['TAVILY_API_KEY'] = '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'

from temple_agent import TempleAgent

def test_agent():
    print("=" * 70)
    print("Temple Agent - Simple Test")
    print("=" * 70)
    print()
    
    # Create agent (verbose=False to avoid Unicode issues)
    agent = TempleAgent(verbose=False)
    
    # Test queries
    queries = [
        "What is the ticket price for Meenakshi Temple?",
        "Tell me about the history of Meenakshi Temple",
        "Tell me about Meenakshi Temple and how to visit"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\nQuery {i}: {query}")
        print("-" * 70)
        
        try:
            response = agent.respond(query)
            
            print(f"Strategy: {response['strategy']}")
            print(f"Temple: {response['temple']}")
            print(f"Confidence: {response['confidence']:.0%}")
            print(f"Quality: {response['quality']}/10")
            print(f"\nAnswer (first 150 chars):")
            print(response['response'][:150] + "...")
            print()
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Show stats
    print("\n" + "=" * 70)
    print("Agent Statistics")
    print("=" * 70)
    stats = agent.get_stats()
    print(f"Total queries: {stats['total_queries']}")
    print(f"Strategies used: {stats['strategies_used']}")
    print(f"Temples discussed: {stats['temples_discussed']}")
    
    print("\n[OK] Agent test complete!")

if __name__ == "__main__":
    test_agent()
