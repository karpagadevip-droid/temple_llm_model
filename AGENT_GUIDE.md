# Temple Agent - Understanding ReAct Pattern

## What is an Agent?

An **agent** is an AI system that can:
- **Think** about what to do
- **Act** by using tools
- **Observe** the results
- **Decide** what to do next

Think of it like a smart assistant that doesn't just answer questions, but figures out HOW to answer them.

---

## ReAct Pattern: Reasoning + Acting

**ReAct** = **Rea**soning + **Act**ing

### The Loop:

```
1. THINK  -> What do I need to do?
2. ACT    -> Execute the action
3. OBSERVE -> Did it work?
4. RESPOND -> Give the answer
```

### Example:

**User**: "What is the ticket price for Meenakshi Temple?"

**Agent's Internal Process**:

1. **THINK**: "This asks about pricing -> need real-time info -> use search"
2. **ACT**: Calls Tavily search API
3. **OBSERVE**: Got result, quality is good
4. **RESPOND**: "Entry fee is Rs 100..."

---

## Chain of Thought (CoT)

**Chain of Thought** = Showing your reasoning step-by-step

### Without CoT:
```
User: What is the ticket price?
Agent: Entry fee is Rs 100
```

### With CoT:
```
User: What is the ticket price?

[THINK] Query asks about pricing -> need real-time info -> use search
[ACT] Executing search tool...
[OBSERVE] Quality: 10/10
[RESPOND] Entry fee is Rs 100
```

**Why it's useful**:
- Makes AI decisions transparent
- Helps debug problems
- Builds trust with users
- Great for interviews!

---

## Tool Selection

The agent has 3 tools:

| Tool | When to Use | Example |
|------|-------------|---------|
| **search** | Real-time info | Ticket prices, timings |
| **model** | Historical facts | Temple history, architecture |
| **hybrid** | Both needed | "Tell me about X and how to visit" |

### How it Decides:

```python
def think(self, query):
    # Analyze keywords
    if "ticket" in query or "price" in query:
        return "search"  # Need current info
    
    elif "history" in query or "built" in query:
        return "model"  # Use fine-tuned knowledge
    
    elif "visit" in query and "about" in query:
        return "hybrid"  # Need both!
```

---

## TempleAgent Architecture

```
TempleAgent
├── think()     -> Reasoning
├── act()       -> Tool execution
├── observe()   -> Quality check
└── respond()   -> Final answer

Tools:
├── search      -> Tavily API
├── model       -> Fine-tuned Llama
└── hybrid      -> Both combined

Memory:
└── conversation_history[]  -> Context tracking
```

---

## Code Example

### Basic Usage:

```python
from temple_agent import TempleAgent

# Create agent
agent = TempleAgent(verbose=True)  # Show reasoning

# Ask question
response = agent.respond("What is the ticket price for Meenakshi Temple?")

# Output:
# [THINK] Query asks about pricing -> use search
# [ACT] Executing search tool...
# [OBSERVE] Quality: 10/10
# [RESPOND] Entry fee is Rs 100...

print(response['response'])
```

### With Statistics:

```python
# Ask multiple questions
agent.respond("What is the ticket price?")
agent.respond("Tell me the history")
agent.respond("How do I visit?")

# Get stats
stats = agent.get_stats()
print(f"Queries: {stats['total_queries']}")
print(f"Strategies: {stats['strategies_used']}")
# Output:
# Queries: 3
# Strategies: {'search': 1, 'model': 1, 'hybrid': 1}
```

---

## Interview Prep

### Q: "What's the difference between RAG and an Agent?"

**Answer**: 
- **RAG** = Retrieval + Generation (passive)
  - You ask, it retrieves and answers
  
- **Agent** = Reasoning + Acting (active)
  - It thinks about HOW to answer
  - Selects the right tool
  - Can use multiple tools in sequence

### Q: "How does your agent decide which tool to use?"

**Answer**:
"My agent uses keyword analysis and query classification. For example:
- Pricing/timing keywords -> search (real-time data)
- History/architecture keywords -> model (trained knowledge)
- Combined queries -> hybrid approach

The decision is made in the `think()` step using Chain of Thought reasoning."

### Q: "What is Chain of Thought?"

**Answer**:
"Chain of Thought is making the AI's reasoning transparent by showing step-by-step thinking. Instead of just giving an answer, it shows:
1. What it understood
2. Why it chose a specific approach
3. What it did
4. How it evaluated the result

This makes the system debuggable and trustworthy."

---

## Key Concepts Summary

| Concept | Definition | Example |
|---------|------------|---------|
| **Agent** | AI that reasons and acts | TempleAgent |
| **ReAct** | Reasoning + Acting pattern | Think -> Act -> Observe |
| **CoT** | Chain of Thought | Show reasoning steps |
| **Tool Selection** | Choosing the right tool | search vs model vs hybrid |
| **Conversation Memory** | Tracking context | Remember previous temples |

---

## Comparison: Before vs After

### Before (Day 4 - RAG Only):

```python
rag = TempleRAG()
result = rag.generate_response("What is the ticket price?")
# Just gets the answer
```

### After (Day 5 - Agent):

```python
agent = TempleAgent(verbose=True)
result = agent.respond("What is the ticket price?")

# Shows:
# [THINK] Need real-time info
# [ACT] Using search
# [OBSERVE] Quality check
# [RESPOND] Final answer
```

**Benefit**: Transparency + Intelligence!

---

## Real-World Applications

**Where agents are used**:
- Customer service bots (think about which department to route to)
- Code assistants (decide which tool to use: search docs, run code, etc.)
- Research assistants (plan multi-step research)
- Personal assistants (break down complex tasks)

**Your Temple Agent**:
- Decides: search vs model vs hybrid
- Tracks conversation context
- Assesses answer quality
- Provides transparent reasoning

---

## Next Steps

**Day 6**: Streamlit UI
- Build web interface
- Deploy the agent
- Make it user-friendly
- Add conversation history display

**Future Enhancements**:
- Multi-turn conversations
- Follow-up questions
- Clarification requests
- Learning from feedback

---

## Resources

**Learn More**:
- ReAct Paper: "ReAct: Synergizing Reasoning and Acting in Language Models"
- Chain of Thought: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- Agent Frameworks: LangChain, AutoGPT, BabyAGI

**Your Implementation**:
- `temple_agent.py` - Main agent class
- `demo_agent.py` - Full demonstration
- `test_agent_simple.py` - Simple test

---

**Congratulations!** You've built an intelligent agent with ReAct pattern! 🎉
