"""
Temple Expert AI - Streamlit Web Interface
Interactive chat application with Chain of Thought reasoning display
"""

import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import temple agent
from temple_agent import TempleAgent
from rag_orchestrator import TempleRAG

# Page configuration
st.set_page_config(
    page_title="Temple Expert AI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .cot-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
    
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if "current_model" not in st.session_state:
    st.session_state.current_model = None

if "show_cot" not in st.session_state:
    st.session_state.show_cot = True

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Model selection
    st.subheader("🤖 Model Selection")
    model_options = {
        "60-step (baseline)": "Karpagadevi/llama-3-temple-expert",
        "600-step (improved)": "Karpagadevi/llama-3-temple-expert-600"
    }
    
    model_choice = st.selectbox(
        "Choose Model",
        list(model_options.keys()),
        index=1  # Default to 600-step
    )
    
    selected_model = model_options[model_choice]
    
    # Load model button
    if st.button("🔄 Load Model") or st.session_state.agent is None:
        with st.spinner(f"Loading {model_choice}..."):
            try:
                # Check if model needs to be reloaded
                if st.session_state.current_model != selected_model:
                    rag = TempleRAG(load_model=True, model_name=selected_model)
                    st.session_state.agent = TempleAgent(rag_system=rag, verbose=False)
                    st.session_state.current_model = selected_model
                    st.success(f"✅ {model_choice} loaded!")
                else:
                    st.info("Model already loaded!")
            except Exception as e:
                st.error(f"Error loading model: {e}")
                st.info("Loading without model (search only)...")
                st.session_state.agent = TempleAgent(verbose=False)
    
    # Display settings
    st.subheader("👁️ Display Options")
    st.session_state.show_cot = st.checkbox(
        "Show Chain of Thought",
        value=st.session_state.show_cot,
        help="Display agent's reasoning process"
    )
    
    # Statistics
    if st.session_state.agent:
        st.subheader("📊 Statistics")
        
        stats = st.session_state.agent.get_stats()
        
        # Total queries
        st.metric("Total Queries", stats['total_queries'])
        
        # Tavily usage
        tavily_stats = stats['rag_stats']['tavily_usage']
        tavily_used = tavily_stats['searches_used']
        tavily_limit = tavily_stats['free_tier_limit']
        tavily_pct = tavily_stats['percentage_used']
        
        st.metric(
            "Tavily Searches",
            f"{tavily_used}/{tavily_limit}",
            f"{tavily_pct:.1f}% used"
        )
        
        # Strategy breakdown
        if stats['strategies_used']:
            st.write("**Strategies Used:**")
            for strategy, count in stats['strategies_used'].items():
                st.write(f"- {strategy}: {count}")
        
        # Temples discussed
        if stats['temples_discussed']:
            st.write("**Temples Discussed:**")
            for temple in stats['temples_discussed'][:5]:  # Show first 5
                st.write(f"- {temple}")
    
    # Clear conversation
    st.subheader("🗑️ Actions")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        if st.session_state.agent:
            st.session_state.agent.clear_history()
        st.rerun()

# Main content
st.markdown('<div class="main-header">🏛️ Temple Expert AI Assistant</div>', unsafe_allow_html=True)

# Info message
if not st.session_state.agent:
    st.info("👈 Please load a model from the sidebar to get started!")
else:
    st.success(f"✅ Using: {model_choice}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # Show Chain of Thought if available and enabled
        if message["role"] == "assistant" and "metadata" in message and st.session_state.show_cot:
            metadata = message["metadata"]
            
            with st.expander("🧠 Chain of Thought", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Reasoning**: {metadata.get('reasoning', 'N/A')}")
                    st.write(f"**Strategy**: {metadata.get('strategy', 'N/A')}")
                
                with col2:
                    st.write(f"**Confidence**: {metadata.get('confidence', 0):.0%}")
                    st.write(f"**Quality**: {metadata.get('quality', 0)}/10")
                
                if metadata.get('temple'):
                    st.write(f"**Temple Identified**: {metadata['temple']}")

# Chat input
if prompt := st.chat_input("Ask about Indian temples..."):
    if not st.session_state.agent:
        st.error("Please load a model first!")
    else:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.agent.respond(prompt, show_reasoning=False)
                    
                    # Display response
                    st.write(response['response'])
                    
                    # Show Chain of Thought if enabled
                    if st.session_state.show_cot:
                        with st.expander("🧠 Chain of Thought", expanded=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Reasoning**: {response['reasoning']}")
                                st.write(f"**Strategy**: {response['strategy']}")
                            
                            with col2:
                                st.write(f"**Confidence**: {response['confidence']:.0%}")
                                st.write(f"**Quality**: {response['quality']}/10")
                            
                            if response.get('temple'):
                                st.write(f"**Temple Identified**: {response['temple']}")
                    
                    # Add assistant message to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response['response'],
                        "metadata": {
                            "reasoning": response['reasoning'],
                            "strategy": response['strategy'],
                            "confidence": response['confidence'],
                            "quality": response['quality'],
                            "temple": response.get('temple')
                        }
                    })
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.write("Please try again or check your API keys in the .env file.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ using Streamlit | Powered by Llama-3 & Tavily AI</p>
    <p><small>Day 6: UI & Deployment - Temple Expert POC</small></p>
</div>
""", unsafe_allow_html=True)
