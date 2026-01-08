"""
Test Suite for RAG System
Tests Tavily search, query classification, and end-to-end RAG
"""

import sys
import argparse
from tavily_search import TavilySearcher
from rag_orchestrator import TempleRAG


def test_search():
    """Test Tavily search functionality"""
    print("=" * 70)
    print("TEST 1: Tavily Search Functionality")
    print("=" * 70)
    print()
    
    try:
        searcher = TavilySearcher()
        print("✅ Tavily client initialized\n")
        
        # Test basic search
        print("Testing: 'Meenakshi Temple ticket price'\n")
        results = searcher.search_temple_tickets("Meenakshi Temple")
        
        if results['success']:
            print("✅ Search successful!")
            print(f"   Found {len(results.get('results', []))} results")
            print(f"   AI Answer: {results.get('answer', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Search failed: {results.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_classification():
    """Test query classification logic"""
    print("\n" + "=" * 70)
    print("TEST 2: Query Classification")
    print("=" * 70)
    print()
    
    try:
        rag = TempleRAG()
        
        test_cases = [
            ("Tell me about Meenakshi Temple", "model"),
            ("What is the ticket price for Meenakshi Temple?", "search"),
            ("Tell me about Meenakshi Temple history and ticket price", "hybrid"),
            ("How to reach Brihadisvara Temple?", "search"),
            ("What is the significance of Tirumala Temple?", "model"),
        ]
        
        all_passed = True
        for query, expected in test_cases:
            result = rag.classify_query(query)
            status = "✅" if result == expected else "❌"
            print(f"{status} '{query[:50]}...'")
            print(f"   Expected: {expected}, Got: {result}")
            if result != expected:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_e2e():
    """Test end-to-end RAG system"""
    print("\n" + "=" * 70)
    print("TEST 3: End-to-End RAG")
    print("=" * 70)
    print()
    
    try:
        rag = TempleRAG()
        
        test_queries = [
            "What is the ticket price for Meenakshi Temple?",
            "Tell me about Meenakshi Temple",
        ]
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 70)
            result = rag.generate_response(query)
            
            if result['success']:
                print(f"✅ Response generated using: {result['source']}")
                print(f"   Preview: {result['response'][:150]}...")
            else:
                print(f"❌ Failed: {result.get('response')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪" * 35)
    print("RAG SYSTEM TEST SUITE")
    print("🧪" * 35)
    print()
    
    results = {
        'search': test_search(),
        'classification': test_classification(),
        'e2e': test_e2e()
    }
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.upper()}: {status}")
    
    all_passed = all(results.values())
    print("\n" + ("🎉 ALL TESTS PASSED!" if all_passed else "⚠️  SOME TESTS FAILED"))
    print("=" * 70)
    
    return all_passed


def main():
    parser = argparse.ArgumentParser(description='Test RAG System')
    parser.add_argument('--test-search', action='store_true', help='Test search only')
    parser.add_argument('--test-classification', action='store_true', help='Test classification only')
    parser.add_argument('--test-e2e', action='store_true', help='Test end-to-end only')
    
    args = parser.parse_args()
    
    if args.test_search:
        success = test_search()
    elif args.test_classification:
        success = test_classification()
    elif args.test_e2e:
        success = test_e2e()
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
