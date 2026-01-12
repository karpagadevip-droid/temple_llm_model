"""
Temple Agent Demo - Interactive demonstration of ReAct pattern
Shows the agent's reasoning process and tool selection
"""

from temple_agent import TempleAgent
from rag_orchestrator import TempleRAG


def demo_basic_queries():
    """Demo 1: Basic queries with different strategies"""
    print("=" * 70)
    print("DEMO 1: Basic Queries with Chain of Thought")
    print("=" * 70)
    print()
    
    # Initialize agent with verbose mode to see reasoning
    agent = TempleAgent(verbose=True)
    
    queries = [
        ("What is the ticket price for Meenakshi Temple?", "search"),
        ("Tell me about the history of Meenakshi Temple", "model"),
        ("Tell me about Meenakshi Temple and how to visit", "hybrid")
    ]
    
    for i, (query, expected_strategy) in enumerate(queries, 1):
        print("\n" + "-" * 70)
        print(f"Query {i}: {query}")
        print(f"Expected strategy: {expected_strategy}")
        print("-" * 70)
        
        response = agent.respond(query)
        
        print(f"\n[RESULT]")
        print(f"Strategy used: {response['strategy']}")
        print(f"Confidence: {response['confidence']:.0%}")
        print(f"Quality: {response['quality']}/10")
        print(f"\nAnswer preview: {response['response'][:150]}...")
        
        # Verify strategy matches expectation
        if response['strategy'] == expected_strategy:
            print("[OK] Strategy matches expectation!")
        else:
            print(f"[WARNING] Expected {expected_strategy}, got {response['strategy']}")


def demo_conversation_memory():
    """Demo 2: Conversation memory"""
    print("\n\n" + "=" * 70)
    print("DEMO 2: Conversation Memory")
    print("=" * 70)
    print()
    
    agent = TempleAgent(verbose=False)
    
    # Multi-turn conversation
    queries = [
        "Tell me about Meenakshi Temple",
        "What about Brihadisvara Temple?",
        "How do I visit the first temple you mentioned?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n[Turn {i}] User: {query}")
        response = agent.respond(query)
        print(f"[Turn {i}] Agent: {response['response'][:100]}...")
        print(f"         Temple: {response['temple']}")
        print(f"         Strategy: {response['strategy']}")
    
    # Show conversation history
    print("\n" + "-" * 70)
    print("Conversation History:")
    print("-" * 70)
    history = agent.get_conversation_history()
    for i, interaction in enumerate(history, 1):
        print(f"{i}. Temple: {interaction['temple']}, Strategy: {interaction['strategy']}")


def demo_agent_stats():
    """Demo 3: Agent statistics"""
    print("\n\n" + "=" * 70)
    print("DEMO 3: Agent Statistics")
    print("=" * 70)
    print()
    
    agent = TempleAgent(verbose=False)
    
    # Run several queries
    queries = [
        "What is the ticket price for Golden Temple?",
        "Tell me about the architecture of Konark Sun Temple",
        "How do I reach Tirumala Temple?",
        "Tell me about Kedarnath Temple history",
        "What are the timings for Somnath Temple?"
    ]
    
    print("Running 5 queries...")
    for query in queries:
        agent.respond(query, show_reasoning=False)
    
    # Show statistics
    stats = agent.get_stats()
    
    print("\n" + "-" * 70)
    print("Agent Statistics:")
    print("-" * 70)
    print(f"Total queries processed: {stats['total_queries']}")
    print(f"\nStrategies used:")
    for strategy, count in stats['strategies_used'].items():
        print(f"  - {strategy}: {count} times")
    print(f"\nTemples discussed: {', '.join(stats['temples_discussed'])}")
    
    # RAG stats
    rag_stats = stats['rag_stats']
    tavily_stats = rag_stats['tavily_usage']
    print(f"\nTavily searches: {tavily_stats['searches_used']}/{tavily_stats['free_tier_limit']}")


def demo_reasoning_comparison():
    """Demo 4: With vs Without Chain of Thought"""
    print("\n\n" + "=" * 70)
    print("DEMO 4: Chain of Thought Comparison")
    print("=" * 70)
    print()
    
    query = "Tell me about Meenakshi Temple and ticket price"
    
    # Without reasoning
    print("WITHOUT Chain of Thought (verbose=False):")
    print("-" * 70)
    agent = TempleAgent(verbose=False)
    response = agent.respond(query)
    print(f"Answer: {response['response'][:100]}...")
    
    # With reasoning
    print("\n\nWITH Chain of Thought (verbose=True):")
    print("-" * 70)
    agent = TempleAgent(verbose=True)
    response = agent.respond(query)
    print(f"\nFinal answer: {response['response'][:100]}...")


def demo_interactive():
    """Demo 5: Interactive mode"""
    print("\n\n" + "=" * 70)
    print("DEMO 5: Interactive Agent")
    print("=" * 70)
    print()
    print("Ask questions about Indian temples!")
    print("Type 'quit' to exit, 'stats' to see statistics")
    print()
    
    agent = TempleAgent(verbose=True)
    
    while True:
        try:
            query = input("\nYou: ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'quit':
                print("\nGoodbye!")
                break
            
            if query.lower() == 'stats':
                stats = agent.get_stats()
                print(f"\nQueries: {stats['total_queries']}")
                print(f"Strategies: {stats['strategies_used']}")
                print(f"Temples: {stats['temples_discussed']}")
                continue
            
            response = agent.respond(query)
            print(f"\nAgent: {response['response'][:300]}")
            if len(response['response']) > 300:
                print("...")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("TEMPLE AGENT - ReAct Pattern Demonstration")
    print("=" * 70)
    print("\nThis demo shows:")
    print("  1. Chain of Thought reasoning")
    print("  2. Tool selection (search/model/hybrid)")
    print("  3. Conversation memory")
    print("  4. Agent statistics")
    print("  5. Interactive mode")
    print()
    
    try:
        # Run demos
        demo_basic_queries()
        demo_conversation_memory()
        demo_agent_stats()
        demo_reasoning_comparison()
        
        # Ask if user wants interactive mode
        print("\n\n" + "=" * 70)
        response = input("Would you like to try interactive mode? (y/n): ")
        if response.lower() == 'y':
            demo_interactive()
        
        print("\n" + "=" * 70)
        print("Demo Complete!")
        print("=" * 70)
        print("\nKey Takeaways:")
        print("  [OK] ReAct pattern: Think -> Act -> Observe -> Respond")
        print("  [OK] Chain of Thought makes reasoning transparent")
        print("  [OK] Agent selects tools intelligently")
        print("  [OK] Conversation memory tracks context")
        print("  [OK] Statistics show agent behavior")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure:")
        print("  1. TAVILY_API_KEY is set in .env file")
        print("  2. All dependencies are installed")
        print("  3. RAG system is working")


if __name__ == "__main__":
    main()
