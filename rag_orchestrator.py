"""
RAG Orchestrator for Temple Expert System
Coordinates between fine-tuned model and Tavily search
"""

import re
from typing import Dict, Tuple, Optional
from tavily_search import TavilySearcher


class TempleRAG:
    """
    RAG orchestrator that decides when to use the model vs. live search
    Combines "frozen knowledge" (fine-tuned model) with "live knowledge" (Tavily)
    """
    
    # Keywords that indicate need for live search
    SEARCH_KEYWORDS = [
        'ticket', 'price', 'cost', 'fee', 'entry',
        'timing', 'time', 'open', 'close', 'hours',
        'how to reach', 'directions', 'location', 'address',
        'contact', 'phone', 'website',
        'current', 'now', 'today', 'latest'
    ]
    
    # Keywords that indicate historical/factual queries (use model)
    MODEL_KEYWORDS = [
        'history', 'built', 'architecture', 'deity',
        'significance', 'legend', 'story', 'mythology',
        'festival', 'ritual', 'tradition', 'culture'
    ]
    
    def __init__(self, tavily_api_key: Optional[str] = None):
        """
        Initialize RAG orchestrator
        
        Args:
            tavily_api_key: Optional Tavily API key
        """
        self.searcher = TavilySearcher(api_key=tavily_api_key)
        self.model = None  # Will be set when fine-tuned model is loaded
    
    def classify_query(self, query: str) -> str:
        """
        Classify query to determine routing strategy
        
        Args:
            query: User query
        
        Returns:
            'search' - Use Tavily search only
            'model' - Use fine-tuned model only
            'hybrid' - Use both model and search
        """
        query_lower = query.lower()
        
        # Check for search keywords
        has_search_keywords = any(
            keyword in query_lower for keyword in self.SEARCH_KEYWORDS
        )
        
        # Check for model keywords
        has_model_keywords = any(
            keyword in query_lower for keyword in self.MODEL_KEYWORDS
        )
        
        # Decision logic
        if has_search_keywords and has_model_keywords:
            return 'hybrid'  # e.g., "Tell me about Meenakshi Temple and ticket price"
        elif has_search_keywords:
            return 'search'  # e.g., "What is the ticket price?"
        elif has_model_keywords:
            return 'model'   # e.g., "Tell me the history of Meenakshi Temple"
        else:
            # Default: if query mentions a temple name, use model
            # Otherwise use hybrid to be safe
            return 'model' if self._contains_temple_name(query) else 'hybrid'
    
    def _contains_temple_name(self, query: str) -> bool:
        """
        Check if query contains a temple name
        Simple heuristic: looks for capitalized words + "temple"
        """
        return 'temple' in query.lower()
    
    def extract_temple_name(self, query: str) -> Optional[str]:
        """
        Extract temple name from query
        
        Args:
            query: User query
        
        Returns:
            Temple name if found, None otherwise
        """
        # Pattern: Capitalized words before "Temple"
        pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+Temple'
        match = re.search(pattern, query)
        
        if match:
            return match.group(1) + " Temple"
        
        # Fallback: look for common temple names
        query_lower = query.lower()
        if 'meenakshi' in query_lower:
            return 'Meenakshi Temple'
        elif 'brihadisvara' in query_lower or 'brihadeeswarar' in query_lower:
            return 'Brihadisvara Temple'
        elif 'tirumala' in query_lower or 'tirupati' in query_lower:
            return 'Tirumala Venkateswara Temple'
        
        return None
    
    def generate_response(self, query: str) -> Dict:
        """
        Generate response using appropriate strategy
        
        Args:
            query: User query
        
        Returns:
            Dict with response, source, and metadata
        """
        # Classify query
        strategy = self.classify_query(query)
        temple_name = self.extract_temple_name(query)
        
        print(f"🔍 Query: {query}")
        print(f"📊 Strategy: {strategy}")
        print(f"🏛️  Temple: {temple_name or 'Not identified'}\n")
        
        if strategy == 'search':
            return self._search_only_response(query, temple_name)
        elif strategy == 'model':
            return self._model_only_response(query, temple_name)
        else:  # hybrid
            return self._hybrid_response(query, temple_name)
    
    def _search_only_response(self, query: str, temple_name: Optional[str]) -> Dict:
        """
        Generate response using Tavily search only
        """
        print("🌐 Using Tavily search...\n")
        
        # Determine search type
        query_lower = query.lower()
        if any(kw in query_lower for kw in ['ticket', 'price', 'fee', 'timing', 'hours']):
            search_results = self.searcher.search_temple_tickets(temple_name or query)
        elif any(kw in query_lower for kw in ['location', 'reach', 'directions', 'address']):
            search_results = self.searcher.search_temple_location(temple_name or query)
        else:
            search_results = self.searcher.search_temple_info(query)
        
        if search_results['success']:
            formatted = self.searcher.format_search_results(search_results)
            return {
                'response': formatted,
                'source': 'tavily_search',
                'strategy': 'search',
                'success': True,
                'temple_name': temple_name
            }
        else:
            return {
                'response': f"Sorry, I couldn't find current information. Error: {search_results.get('error')}",
                'source': 'error',
                'strategy': 'search',
                'success': False,
                'temple_name': temple_name
            }
    
    def _model_only_response(self, query: str, temple_name: Optional[str]) -> Dict:
        """
        Generate response using fine-tuned model only
        """
        print("🧠 Using fine-tuned model...\n")
        
        if self.model is None:
            return {
                'response': (
                    "The fine-tuned model is not loaded yet. "
                    "This would normally provide historical and cultural information about the temple."
                ),
                'source': 'model_placeholder',
                'strategy': 'model',
                'success': False,
                'temple_name': temple_name
            }
        
        # TODO: Integrate with actual fine-tuned model
        # For now, return placeholder
        return {
            'response': "[Model response would appear here]",
            'source': 'model',
            'strategy': 'model',
            'success': True,
            'temple_name': temple_name
        }
    
    def _hybrid_response(self, query: str, temple_name: Optional[str]) -> Dict:
        """
        Generate response using both model and search
        """
        print("🔄 Using hybrid approach (model + search)...\n")
        
        # Get model response
        model_response = self._model_only_response(query, temple_name)
        
        # Get search response
        search_response = self._search_only_response(query, temple_name)
        
        # Combine responses
        combined = "**Historical Information:**\n"
        combined += model_response['response'] + "\n\n"
        combined += "**Current Information:**\n"
        combined += search_response['response']
        
        return {
            'response': combined,
            'source': 'hybrid',
            'strategy': 'hybrid',
            'success': model_response['success'] or search_response['success'],
            'temple_name': temple_name
        }
    
    def get_stats(self) -> Dict:
        """
        Get usage statistics
        """
        return {
            'tavily_usage': self.searcher.get_usage_stats(),
            'model_loaded': self.model is not None
        }


def main():
    """
    Demo function to test RAG orchestrator
    """
    print("=" * 70)
    print("Temple RAG Orchestrator - Demo")
    print("=" * 70)
    print()
    
    try:
        # Initialize RAG
        rag = TempleRAG()
        
        # Test queries
        test_queries = [
            "Tell me about Meenakshi Temple",  # Should use model
            "What is the ticket price for Meenakshi Temple?",  # Should use search
            "Tell me about Meenakshi Temple history and ticket price",  # Should use hybrid
        ]
        
        for query in test_queries:
            print("=" * 70)
            result = rag.generate_response(query)
            print(f"✅ Response ({result['source']}):\n")
            print(result['response'])
            print("\n")
        
        # Show stats
        print("=" * 70)
        print("Usage Statistics:")
        stats = rag.get_stats()
        tavily_stats = stats['tavily_usage']
        print(f"Tavily searches: {tavily_stats['searches_used']}/{tavily_stats['free_tier_limit']}")
        print(f"Model loaded: {stats['model_loaded']}")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to:")
        print("1. Set up Tavily API key in .env file")
        print("2. Install required packages: pip install tavily-python python-dotenv")


if __name__ == "__main__":
    main()
