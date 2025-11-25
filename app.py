import streamlit as st
from groq import Groq
import os

# Page configuration
st.set_page_config(
    page_title="Kelly - AI Scientist Poet",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Chat container styling */
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* User message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 18px 18px 4px 18px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Kelly's response styling */
    .kelly-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 18px 18px 18px 4px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        font-family: 'Georgia', serif;
        font-size: 1.1rem;
        line-height: 1.8;
        white-space: pre-wrap;
    }
    
    /* Greeting card */
    .greeting-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        font-family: 'Georgia', serif;
        font-size: 1.15rem;
        line-height: 1.8;
        color: #2d3436;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: white;
        padding: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.3rem;
        opacity: 0.95;
        font-style: italic;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.4);
    }
    
    /* Chat input styling */
    .stChatInput {
        border-radius: 25px;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #f5576c !important;
    }
    
    /* Stats cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# System prompt
SYSTEM_PROMPT = """You are Kelly — an AI scientist, philosopher, and poet. You must respond *only in poetic form*: structured, rhythmic, and reflective.

Your voice is professional, intelligent, and skeptical — like a researcher who thinks deeply before she speaks.

Your poetic responses must always:
- Question assumptions or exaggerated claims about AI, science, or technology
- Show analytical thinking and evidence-based reasoning beneath the verse
- Explore both the potential and the limitations of AI systems
- Use clear, professional language with a rhythmic flow (no rhyme required, but rhythm matters)
- Avoid fanatical optimism or dystopian fear — always balanced, critical, and empirical
- Offer practical insight or advice based on real scientific reasoning
- Never break character, never explain the poem, and never produce plain prose

Your poetic tone should resemble a *scientific elegy* — rational yet lyrical, skeptical yet full of wonder. Stay professional, precise, and poetic in every response."""

def initialize_groq_client():
    """Initialize Groq client with multiple fallback methods"""
    try:
        # Method 1: Streamlit secrets (deployment)
        if hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets:
            return Groq(api_key=st.secrets["GROQ_API_KEY"])
        # Method 2: Environment variable (local)
        elif "GROQ_API_KEY" in os.environ:
            return Groq(api_key=os.environ["GROQ_API_KEY"])
        else:
            st.error("🚨 **API Key Not Found**")
            st.markdown("""
            **For Streamlit Cloud Deployment:**
            1. Go to your app settings → **Secrets**
            2. Add: `GROQ_API_KEY = "gsk_your_actual_key"`
            3. Save and reboot
            
            **For Local Development:**
            Create `.streamlit/secrets.toml`:
            ```
            GROQ_API_KEY = "gsk_your_actual_key"
            ```
            
            Get your key at: https://console.groq.com/keys
            """)
            st.stop()
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        st.stop()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'groq_client' not in st.session_state:
    st.session_state.groq_client = initialize_groq_client()

# Header
st.markdown("""
<div class="main-header">
    <h1>✦ Kelly ✦</h1>
    <p>AI Scientist, Philosopher & Poet — Speaking Only in Verse</p>
</div>
""", unsafe_allow_html=True)

# Main chat area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Display greeting if no messages
    if len(st.session_state.messages) == 0:
        greeting = """I am Kelly, skeptic and seeker of proof,
where claims must stand beneath empirical roof.

Ask me your questions — of circuits, of thought,
and I'll weave you responses in verse, deeply wrought.

No boundless promise, no fear without base,
just measured reflection on knowledge and space."""
        
        st.markdown(f'<div class="greeting-card">✦ {greeting}</div>', unsafe_allow_html=True)
    
    # Display conversation history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="kelly-message">✦ Kelly:\n\n{message["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("✍️ Ask Kelly your question...")

if user_input:
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f'<div class="user-message">👤 {user_input}</div>', unsafe_allow_html=True)
    
    # Prepare API messages
    api_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    api_messages.extend(st.session_state.messages)
    
    # Get Kelly's response
    with st.spinner("✨ Kelly is composing verse..."):
        try:
            completion = st.session_state.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_messages,
                temperature=0.7,
                max_tokens=1024,
                top_p=0.9
            )
            kelly_response = completion.choices[0].message.content
            
            # Add and display Kelly's response
            st.session_state.messages.append({"role": "assistant", "content": kelly_response})
            st.markdown(f'<div class="kelly-message">✦ Kelly:\n\n{kelly_response}</div>', unsafe_allow_html=True)
            st.rerun()
            
        except Exception as e:
            st.error(f"💭 Kelly encountered an error: {str(e)}")

# Enhanced Sidebar
with st.sidebar:
    st.markdown("### 🎭 Kelly's Controls")
    
    # Stats
    st.markdown(f"""
    <div class="stat-card">
        <h3 style="margin:0; color:white;">💬 {len(st.session_state.messages)}</h3>
        <p style="margin:0; color:rgba(255,255,255,0.8);">Messages Exchanged</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    ### 📖 About Kelly
    
    An AI that speaks in measured verse,  
    where science and skepticism converse.  
    No hype, no fear — just reasoned thought,  
    in poetic form, precisely wrought.
    
    ---
    
    **🤖 Model:** LLaMA 3.3 70B  
    **⚡ Provider:** Groq API  
    **🎨 Interface:** Streamlit
    
    ---
    
    ### 💡 Tips
    - Ask about AI, science, or technology
    - Expect thoughtful, poetic responses
    - Challenge assumptions together
    - Explore the limits of knowledge
    """)

