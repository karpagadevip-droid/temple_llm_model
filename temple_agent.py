"""
Temple Agent - Intelligent Agent with ReAct Pattern
Implements Reasoning + Acting for temple information queries
"""

from collections import deque
from datetime import datetime
from typing import Dict, List, Optional
from rag_orchestrator import TempleRAG


class TempleAgent:
    """
    Intelligent agent for temple information using ReAct pattern
    
    ReAct Loop:
    1. THINK - Reason about what to do
    2. ACT - Execute the action using appropriate tool
    3. OBSERVE - Check if result is satisfactory
    4. RESPOND - Format and return answer
    
    Tools Available:
    - search: Real-time information (Tavily)
    - model: Historical/cultural information (Fine-tuned Llama)
    - hybrid: Combined approach
    """
    
    def __init__(self, rag_system: Optional[TempleRAG] = None, verbose: bool = False):
        """
        Initialize Temple Agent
        
        Args:
            rag_system: RAG orchestrator (creates one if not provided)
            verbose: Show Chain of Thought reasoning
        """
        self.rag = rag_system or TempleRAG()
        self.verbose = verbose
        # Use deque with maxlen for automatic size limiting
        self.conversation_history = deque(maxlen=10)
        
        # Tool registry - maps tool names to RAG methods
        self.tools = {
            'search': self._use_search,
            'model': self._use_model,
            'hybrid': self._use_hybrid
        }
    
    def think(self, query: str) -> Dict:
        """
        THINK step - Reason about what to do
        
        Analyzes the query and decides on the best approach
        
        Args:
            query: User's question
        
        Returns:
            Thought process with reasoning and plan
        """
        # Analyze query using RAG classifier
        strategy = self.rag.classify_query(query)
        temple_name = self.rag.extract_temple_name(query)
        
        # Build reasoning
        reasoning = self._explain_strategy_choice(query, strategy, temple_name)
        
        thought = {
            'query': query,
            'temple_identified': temple_name,
            'tool_selected': strategy,
            'reasoning': reasoning,
            'confidence': self._assess_confidence(query, strategy)
        }
        
        if self.verbose:
            print(f"\n[THINK] {reasoning}")
            print(f"[PLAN] Use '{strategy}' tool")
            if temple_name:
                print(f"[CONTEXT] Temple: {temple_name}")
        
        return thought
    
    def act(self, thought: Dict) -> Dict:
        """
        ACT step - Execute the plan
        
        Uses the selected tool to get information
        
        Args:
            thought: Output from think() step
        
        Returns:
            Result from tool execution
        """
        tool_name = thought['tool_selected']
        query = thought['query']
        
        if self.verbose:
            print(f"\n[ACT] Executing {tool_name} tool...")
        
        # Execute the selected tool
        tool_function = self.tools.get(tool_name)
        if not tool_function:
            return {
                'success': False,
                'error': f"Unknown tool: {tool_name}",
                'response': "I'm not sure how to answer that."
            }
        
        result = tool_function(query)
        
        if self.verbose:
            source = result.get('source', 'unknown')
            print(f"[ACT] Got response from: {source}")
        
        return result
    
    def observe(self, result: Dict, thought: Dict) -> Dict:
        """
        OBSERVE step - Check if result is satisfactory
        
        Evaluates the quality and completeness of the result
        
        Args:
            result: Output from act() step
            thought: Original thought process
        
        Returns:
            Observation with quality assessment
        """
        # Assess result quality
        quality_score = self._assess_quality(result)
        is_complete = self._check_completeness(result, thought)
        
        observation = {
            'success': result.get('success', False),
            'quality_score': quality_score,
            'is_complete': is_complete,
            'needs_followup': not is_complete,
            'result': result
        }
        
        if self.verbose:
            print(f"\n[OBSERVE] Quality: {quality_score}/10")
            print(f"[OBSERVE] Complete: {'Yes' if is_complete else 'No'}")
        
        return observation
    
    def respond(self, query: str, show_reasoning: bool = None) -> Dict:
        """
        Main entry point - Complete ReAct loop
        
        Args:
            query: User's question
            show_reasoning: Override verbose setting for this query
        
        Returns:
            Final response with metadata
        """
        # Use instance verbose if not overridden
        original_verbose = self.verbose
        if show_reasoning is not None:
            self.verbose = show_reasoning
        
        try:
            # ReAct Loop
            thought = self.think(query)
            action_result = self.act(thought)
            observation = self.observe(action_result, thought)
            
            # Format final response
            response = self._format_response(observation, thought)
            
            # Add to conversation memory
            self._add_to_memory(query, response)
            
            if self.verbose:
                print(f"\n[RESPOND] Returning answer to user")
            
            return response
            
        finally:
            # Restore original verbose setting
            self.verbose = original_verbose
    
    # ============================================================
    # Tool Execution Methods
    # ============================================================
    
    def _use_search(self, query: str) -> Dict:
        """Use Tavily search for real-time information"""
        return self.rag._search_only_response(query, self.rag.extract_temple_name(query))
    
    def _use_model(self, query: str) -> Dict:
        """Use fine-tuned model for historical information"""
        return self.rag._model_only_response(query, self.rag.extract_temple_name(query))
    
    def _use_hybrid(self, query: str) -> Dict:
        """Use both model and search"""
        return self.rag._hybrid_response(query, self.rag.extract_temple_name(query))
    
    # ============================================================
    # Reasoning and Assessment Methods
    # ============================================================
    
    def _explain_strategy_choice(self, query: str, strategy: str, temple_name: Optional[str]) -> str:
        """
        Generate human-readable explanation of strategy choice
        (Chain of Thought reasoning)
        """
        query_lower = query.lower()
        
        if strategy == 'search':
            if any(kw in query_lower for kw in ['ticket', 'price', 'fee']):
                return "Query asks about pricing â†’ need real-time info â†’ use search"
            elif any(kw in query_lower for kw in ['timing', 'hours', 'open']):
                return "Query asks about timings â†’ need current info â†’ use search"
            elif any(kw in query_lower for kw in ['location', 'reach', 'directions']):
                return "Query asks about location/directions â†’ use search"
            else:
                return "Query needs real-time information â†’ use search"
        
        elif strategy == 'model':
            if any(kw in query_lower for kw in ['history', 'built']):
                return "Query asks about history â†’ use fine-tuned model knowledge"
            elif any(kw in query_lower for kw in ['architecture', 'deity']):
                return "Query asks about cultural/architectural details â†’ use model"
            else:
                return "Query about temple facts â†’ use model knowledge"
        
        else:  # hybrid
            return "Query needs both historical context and current info -> use hybrid approach"
    
    def _assess_confidence(self, query: str, strategy: str) -> float:
        """Assess confidence in strategy selection (0-1)"""
        query_lower = query.lower()
        
        # High confidence keywords
        high_conf_search = ['ticket', 'price', 'timing', 'hours', 'location']
        high_conf_model = ['history', 'built', 'architecture', 'deity', 'significance']
        
        if strategy == 'search' and any(kw in query_lower for kw in high_conf_search):
            return 0.95
        elif strategy == 'model' and any(kw in query_lower for kw in high_conf_model):
            return 0.95
        elif strategy == 'hybrid':
            return 0.85
        else:
            return 0.70
    
    def _assess_quality(self, result: Dict) -> int:
        """Assess quality of result (1-10 scale)"""
        if not result.get('success'):
            return 2
        
        response = result.get('response', '')
        
        # Quality indicators
        has_content = len(response) > 50
        has_sources = 'Source:' in response or 'http' in response
        not_error = 'error' not in response.lower()
        not_placeholder = 'placeholder' not in response.lower()
        
        score = 5  # Base score
        if has_content:
            score += 2
        if has_sources:
            score += 2
        if not_error:
            score += 1
        if not not_placeholder:
            score -= 3
        
        return max(1, min(10, score))
    
    def _check_completeness(self, result: Dict, thought: Dict) -> bool:
        """Check if result fully answers the query"""
        if not result.get('success'):
            return False
        
        response = result.get('response', '')
        
        # Basic completeness checks
        has_substantial_content = len(response) > 30
        not_error_message = 'error' not in response.lower()
        not_placeholder = 'placeholder' not in response.lower()
        
        return has_substantial_content and not_error_message and not_placeholder
    
    def _format_response(self, observation: Dict, thought: Dict) -> Dict:
        """Format final response with metadata"""
        result = observation['result']
        
        return {
            'response': result.get('response', ''),
            'source': result.get('source', 'unknown'),
            'strategy': thought['tool_selected'],
            'temple': thought['temple_identified'],
            'confidence': thought['confidence'],
            'quality': observation['quality_score'],
            'reasoning': thought['reasoning'],
            'success': observation['success']
        }
    
    # ============================================================
    # Conversation Memory
    # ============================================================
    
    def _add_to_memory(self, query: str, response: Dict):
        """Add interaction to conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'query': query,
            'response': response['response'],
            'strategy': response['strategy'],
            'temple': response['temple']
        })
        # No trimming needed - deque automatically removes oldest when full!
    
    def get_conversation_history(self, last_n: int = 5) -> List[Dict]:
        """Get recent conversation history"""
        # Convert deque to list for slicing
        return list(self.conversation_history)[-last_n:]
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    # ============================================================
    # Utility Methods
    # ============================================================
    
    def get_stats(self) -> Dict:
        """Get agent statistics"""
        if not self.conversation_history:
            return {
                'total_queries': 0,
                'strategies_used': {},
                'temples_discussed': set()
            }
        
        strategies = {}
        temples = set()
        
        for interaction in self.conversation_history:
            strategy = interaction['strategy']
            strategies[strategy] = strategies.get(strategy, 0) + 1
            
            if interaction['temple']:
                temples.add(interaction['temple'])
        
        return {
            'total_queries': len(self.conversation_history),
            'strategies_used': strategies,
            'temples_discussed': list(temples),
            'rag_stats': self.rag.get_stats()
        }


def main():
    """Demo: Temple Agent with ReAct pattern"""
    print("=" * 70)
    print("Temple Agent - ReAct Pattern Demo")
    print("=" * 70)
    print()
    
    # Initialize agent with verbose mode
    agent = TempleAgent(verbose=True)
    
    # Test queries
    queries = [
        "What is the ticket price for Meenakshi Temple?",
        "Tell me about the history of Meenakshi Temple",
        "Tell me about Meenakshi Temple and how to visit"
    ]
    
    for i, query in enumerate(queries, 1):
        print("\n" + "=" * 70)
        print(f"Query {i}: {query}")
        print("=" * 70)
        
        response = agent.respond(query)
        
        print(f"\n[FINAL RESPONSE]")
        print(f"Answer: {response['response'][:200]}...")
        print(f"Confidence: {response['confidence']:.0%}")
        print(f"Quality: {response['quality']}/10")
    
    # Show stats
    print("\n" + "=" * 70)
    print("Agent Statistics")
    print("=" * 70)
    stats = agent.get_stats()
    print(f"Total queries: {stats['total_queries']}")
    print(f"Strategies used: {stats['strategies_used']}")
    print(f"Temples discussed: {stats['temples_discussed']}")


if __name__ == "__main__":
    main()

