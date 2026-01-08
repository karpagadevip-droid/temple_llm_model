"""
Tavily Search Module for Temple RAG System
Provides AI-optimized web search for real-time temple information
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TavilySearcher:
    """
    Handles Tavily AI search integration for temple information
    Tavily provides AI-optimized, cleaned search results perfect for RAG
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Tavily searcher
        
        Args:
            api_key: Tavily API key (if not provided, reads from TAVILY_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Tavily API key not found. Please set TAVILY_API_KEY environment variable "
                "or pass api_key parameter. Get your free API key at https://tavily.com/"
            )
        
        # Import tavily-python library
        try:
            from tavily import TavilyClient
            self.client = TavilyClient(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "tavily-python library not found. Install it with: pip install tavily-python"
            )
        
        # Track search usage (free tier: 1000 searches/month)
        self.search_count = 0
        self.max_free_searches = 1000
    
    def search_temple_info(
        self, 
        query: str, 
        max_results: int = 5,
        include_domains: Optional[List[str]] = None,
        search_depth: str = "basic"
    ) -> Dict:
        """
        Search for temple information using Tavily AI
        
        Args:
            query: Search query (e.g., "Meenakshi Temple ticket price")
            max_results: Maximum number of results to return (default: 5)
            include_domains: Optional list of domains to prioritize
            search_depth: "basic" (1 credit) or "advanced" (2 credits)
        
        Returns:
            Dict containing search results with AI-optimized content
        """
        try:
            # Increment search counter
            self.search_count += 1
            
            # Warn if approaching free tier limit
            if self.search_count >= self.max_free_searches * 0.9:
                print(f"⚠️  Warning: {self.search_count}/{self.max_free_searches} free searches used")
            
            # Perform search
            response = self.client.search(
                query=query,
                max_results=max_results,
                include_domains=include_domains,
                search_depth=search_depth,
                include_answer=True,  # Get AI-generated answer
                include_raw_content=False  # We don't need raw HTML
            )
            
            return {
                'success': True,
                'query': query,
                'answer': response.get('answer', ''),  # AI-generated summary
                'results': response.get('results', []),
                'search_count': self.search_count
            }
            
        except Exception as e:
            return {
                'success': False,
                'query': query,
                'error': str(e),
                'search_count': self.search_count
            }
    
    def format_search_results(self, search_response: Dict) -> str:
        """
        Format Tavily search results for LLM consumption
        
        Args:
            search_response: Response from search_temple_info()
        
        Returns:
            Formatted string ready for LLM context
        """
        if not search_response.get('success'):
            return f"Search failed: {search_response.get('error', 'Unknown error')}"
        
        # Start with AI-generated answer if available
        formatted = ""
        if search_response.get('answer'):
            formatted += f"**AI Summary:**\n{search_response['answer']}\n\n"
        
        # Add individual search results with citations
        results = search_response.get('results', [])
        if results:
            formatted += "**Sources:**\n"
            for i, result in enumerate(results[:5], 1):
                title = result.get('title', 'No title')
                content = result.get('content', 'No content')
                url = result.get('url', '')
                score = result.get('score', 0)
                
                formatted += f"{i}. **{title}** (Relevance: {score:.2f})\n"
                formatted += f"   {content}\n"
                formatted += f"   Source: {url}\n\n"
        
        return formatted.strip()
    
    def search_temple_tickets(self, temple_name: str) -> Dict:
        """
        Specialized search for temple ticket prices and timings
        
        Args:
            temple_name: Name of the temple
        
        Returns:
            Search results focused on tickets and timings
        """
        query = f"{temple_name} ticket price entry fee timings opening hours"
        
        # Prioritize official tourism and temple websites
        include_domains = [
            'incredibleindia.org',
            'tourism.gov.in',
            'tripadvisor.com',
            'makemytrip.com'
        ]
        
        return self.search_temple_info(
            query=query,
            max_results=5,
            include_domains=include_domains,
            search_depth="basic"
        )
    
    def search_temple_location(self, temple_name: str) -> Dict:
        """
        Specialized search for temple location and how to reach
        
        Args:
            temple_name: Name of the temple
        
        Returns:
            Search results focused on location and directions
        """
        query = f"{temple_name} location address how to reach directions"
        
        return self.search_temple_info(
            query=query,
            max_results=5,
            search_depth="basic"
        )
    
    def get_usage_stats(self) -> Dict:
        """
        Get current usage statistics
        
        Returns:
            Dict with search count and remaining free searches
        """
        return {
            'searches_used': self.search_count,
            'free_tier_limit': self.max_free_searches,
            'remaining': self.max_free_searches - self.search_count,
            'percentage_used': (self.search_count / self.max_free_searches) * 100
        }


def main():
    """
    Demo function to test Tavily search
    """
    print("=" * 60)
    print("Tavily Search Module - Demo")
    print("=" * 60)
    
    try:
        # Initialize searcher
        searcher = TavilySearcher()
        print("✅ Tavily client initialized successfully\n")
        
        # Test search
        print("Testing search: 'Meenakshi Temple ticket price'\n")
        results = searcher.search_temple_tickets("Meenakshi Temple")
        
        if results['success']:
            print("✅ Search successful!\n")
            print(searcher.format_search_results(results))
        else:
            print(f"❌ Search failed: {results.get('error')}")
        
        # Show usage stats
        print("\n" + "=" * 60)
        stats = searcher.get_usage_stats()
        print(f"Usage: {stats['searches_used']}/{stats['free_tier_limit']} "
              f"({stats['percentage_used']:.1f}%)")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure to:")
        print("1. Sign up at https://tavily.com/")
        print("2. Get your API key from the dashboard")
        print("3. Create a .env file with: TAVILY_API_KEY=your_key_here")
        print("4. Install tavily-python: pip install tavily-python")


if __name__ == "__main__":
    main()
