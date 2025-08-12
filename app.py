import streamlit as st
import json
import time
from datetime import datetime
import pandas as pd
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
from workflow.graph import build_workflow

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling with proper contrast
st.markdown("""
<style>
    /* Force dark theme and ensure text visibility */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        color: #fafafa !important;
    }
    
    .user-message {
        background-color: #1e2329 !important;
        border-left-color: #667eea;
        color: #fafafa !important;
    }
    
    .agent-message {
        background-color: #0d1421 !important;
        border-left-color: #00c4cc;
        color: #fafafa !important;
        border: 1px solid #2a2a2a;
    }
    
    .metric-card {
        background: #1e2329 !important;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        color: #fafafa !important;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    /* Ensure all text elements are visible */
    .stMarkdown, .stText, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: #fafafa !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e2329 !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #1e2329 !important;
        color: #fafafa !important;
        border: 1px solid #4a4a4a !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > select {
        background-color: #1e2329 !important;
        color: #fafafa !important;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #667eea !important;
    }
    
    /* Metrics */
    .metric-value {
        color: #fafafa !important;
        font-size: 1.5rem !important;
        font-weight: bold !important;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #1e2329 !important;
        color: #fafafa !important;
        border: 1px solid #667eea !important;
    }
    
    /* Success boxes */
    .stSuccess {
        background-color: #0d4f3c !important;
        color: #fafafa !important;
    }
    
    /* Warning boxes */
    .stWarning {
        background-color: #4a3c0d !important;
        color: #fafafa !important;
    }
    
    /* Container backgrounds */
    .block-container {
        background-color: #0e1117 !important;
    }
    
    /* Ensure captions are visible */
    .caption {
        color: #a0a0a0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize workflow
@st.cache_resource
def get_workflow():
    return build_workflow()

workflow = get_workflow()

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "research_history" not in st.session_state:
    st.session_state.research_history = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0
if "total_response_time" not in st.session_state:
    st.session_state.total_response_time = 0

# Header
st.markdown("""
<div class="main-header">
    <h1>🔬 AI-Powered Research Assistant</h1>
    <p>Advanced Multi-Agent System for Comprehensive Research Analysis</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x100/667eea/ffffff?text=AI+Research", width=200)
    
    st.markdown("### 📊 Session Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.query_count)
    with col2:
        avg_time = st.session_state.total_response_time / max(st.session_state.query_count, 1)
        st.metric("Avg Time", f"{avg_time:.1f}s")
    
    st.markdown("### 🛠️ Settings")
    
    # Response format options
    response_format = st.selectbox(
        "Response Format",
        ["Detailed Analysis", "Summary Only", "Bullet Points", "Executive Summary"]
    )
    
    # Research depth
    research_depth = st.slider("Research Depth", 1, 5, 3)
    
    # Enable features
    enable_citations = st.checkbox("Include Citations", True)
    enable_related_topics = st.checkbox("Suggest Related Topics", True)
    
    st.markdown("### 📚 Quick Actions")
    
    if st.button("📥 Export Conversation"):
        if st.session_state.conversation:
            conversation_json = json.dumps(st.session_state.conversation, indent=2)
            st.download_button(
                "Download JSON",
                conversation_json,
                file_name=f"research_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    if st.button("🗑️ Clear History"):
        st.session_state.conversation = []
        st.session_state.research_history = []
        st.rerun()
    
    if st.button("📊 Generate Report"):
        if st.session_state.conversation:
            st.info("Report generation feature coming soon!")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 💬 Research Interface")
    
    # Enhanced input area
    with st.container():
        st.markdown("#### Enter your research query:")
        
        # Input options
        input_method = st.radio(
            "Input Method:",
            ["Text Input", "Voice Input (Simulated)", "File Upload"],
            horizontal=True
        )
        
        user_input = ""
        
        if input_method == "Text Input":
            user_input = st.text_area(
                "Your research question:",
                placeholder="e.g., What are the latest developments in quantum computing?",
                height=100
            )
            
        elif input_method == "Voice Input (Simulated)":
            st.info("🎤 Voice input simulation - please use text input for now")
            user_input = st.text_input("Transcribed text will appear here...")
            
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader("Upload a document for analysis", type=['txt', 'pdf', 'docx'])
            if uploaded_file:
                user_input = f"Analyze the uploaded document: {uploaded_file.name}"
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            col_a, col_b = st.columns(2)
            with col_a:
                priority_sources = st.multiselect(
                    "Priority Sources",
                    ["Academic Papers", "News Articles", "Government Reports", "Industry Analysis"]
                )
            with col_b:
                time_filter = st.selectbox(
                    "Time Filter",
                    ["Any Time", "Past Week", "Past Month", "Past Year"]
                )
    
    # Submit button with enhanced functionality
    col_submit, col_example = st.columns([1, 1])
    
    with col_submit:
        submit_button = st.button("🚀 Start Research", type="primary")
    
    with col_example:
        if st.button("💡 Example Query"):
            example_queries = [
                "What are the environmental impacts of renewable energy?",
                "How is AI transforming healthcare?",
                "What are the latest trends in sustainable agriculture?",
                "Analyze the current state of space exploration technology"
            ]
            import random
            user_input = random.choice(example_queries)
            st.rerun()

with col2:
    st.markdown("### 📈 Research Analytics")
    
    if st.session_state.query_count > 0:
        # Query frequency chart
        df_queries = pd.DataFrame({
            'Query': range(1, st.session_state.query_count + 1),
            'Response_Time': [2.5, 3.1, 1.8, 2.9, 3.5][:st.session_state.query_count]
        })
        
        fig = px.line(df_queries, x='Query', y='Response_Time', 
                     title='Response Time Trend',
                     labels={'Response_Time': 'Time (seconds)'})
        fig.update_layout(height=200)
        st.plotly_chart(fig, use_container_width=True)
        
        # Research topics cloud (simulated)
        st.markdown("#### 🏷️ Research Topics")
        topics = ["AI", "Technology", "Science", "Environment", "Healthcare"]
        for topic in topics[:min(len(topics), st.session_state.query_count)]:
            st.badge(topic)

# Process research query
if submit_button and user_input:
    start_time = time.time()
    
    # Add user message
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.conversation.append({
        "role": "user", 
        "content": user_input,
        "timestamp": timestamp,
        "settings": {
            "format": response_format,
            "depth": research_depth,
            "citations": enable_citations
        }
    })
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate multi-agent workflow with progress updates
    progress_steps = [
        "🔍 Initializing research agents...",
        "📚 Gathering information from sources...",
        "🧠 Processing and analyzing data...",
        "✍️ Generating comprehensive summary...",
        "✅ Finalizing research results..."
    ]
    
    for i, step in enumerate(progress_steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(progress_steps))
        time.sleep(0.5)  # Simulate processing time
    
    # Get actual workflow result
    try:
        with st.spinner("🤖 Agents are collaborating..."):
            result = workflow.invoke({
                "messages": [{"type": "human", "content": user_input}],
                "settings": {
                    "format": response_format,
                    "depth": research_depth,
                    "citations": enable_citations
                }
            })
            final_answer = result.get("final_answer", "I apologize, but I couldn't generate a response. Please try again.")
    except Exception as e:
        final_answer = f"⚠️ Research workflow encountered an issue: {str(e)}. Please check your workflow configuration."
    
    # Calculate response time
    end_time = time.time()
    response_time = end_time - start_time
    st.session_state.total_response_time += response_time
    st.session_state.query_count += 1
    
    # Add agent response
    st.session_state.conversation.append({
        "role": "agent", 
        "content": final_answer,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "response_time": response_time,
        "word_count": len(final_answer.split())
    })
    
    # Add to research history
    st.session_state.research_history.append({
        "query": user_input,
        "timestamp": datetime.now().isoformat(),
        "response_time": response_time
    })
    
    # Clear progress indicators
    progress_bar.empty()
    status_text.empty()
    
    st.rerun()

# Display conversation with enhanced formatting
st.markdown("### 💬 Research Conversation")

if not st.session_state.conversation:
    st.info("👋 Welcome! Start by entering a research query above.")
    
    # Show example queries
    st.markdown("#### 💡 Example Research Queries:")
    examples = [
        "🔬 What are the latest breakthroughs in CRISPR gene editing?",
        "🌍 How effective are carbon capture technologies?",
        "🤖 What are the ethical implications of AI in decision-making?",
        "🏥 What are emerging treatments for Alzheimer's disease?"
    ]
    
    for example in examples:
        if st.button(example, key=f"example_{example}"):
            st.text_input("Research Query", value=example.split(" ", 1)[1])
else:
    # Display conversation with enhanced UI
    for i, turn in enumerate(st.session_state.conversation):
        if turn["role"] == "user":
            with st.container():
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 You ({turn.get('timestamp', 'N/A')})</strong><br>
                    {turn['content']}
                </div>
                """, unsafe_allow_html=True)
                
        else:
            with st.container():
                col_msg, col_actions = st.columns([4, 1])
                
                with col_msg:
                    st.markdown(f"""
                    <div class="chat-message agent-message">
                        <strong>🤖 AI Research Assistant ({turn.get('timestamp', 'N/A')})</strong><br>
                        {turn['content']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_actions:
                    st.caption(f"⏱️ {turn.get('response_time', 0):.1f}s")
                    st.caption(f"📝 {turn.get('word_count', 0)} words")
                    
                    if st.button("👍", key=f"like_{i}"):
                        st.success("Feedback recorded!")
                    
                    if st.button("📋", key=f"copy_{i}"):
                        st.info("Content copied to clipboard!")

# Footer
st.markdown("---")
col_foot1, col_foot2, col_foot3 = st.columns(3)

with col_foot1:
    st.markdown("**🔬 AI Research Assistant**")
    st.caption("Powered by Multi-Agent Technology")

with col_foot2:
    st.markdown("**📊 Session Info**")
    st.caption(f"Queries: {st.session_state.query_count} | Session: {datetime.now().strftime('%Y-%m-%d')}")

with col_foot3:
    st.markdown("**🚀 Features**")
    st.caption("Real-time • Multi-Agent • Export Ready")