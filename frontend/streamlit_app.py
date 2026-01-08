"""
Resume Coach - Streamlit Frontend Application

Multi-page Streamlit app for AI-powered resume coaching.
"""
import streamlit as st
import requests
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="Resume Coach AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .score-excellent {
        color: #28a745;
        font-size: 3rem;
        font-weight: bold;
    }
    .score-good {
        color: #17a2b8;
        font-size: 3rem;
        font-weight: bold;
    }
    .score-fair {
        color: #ffc107;
        font-size: 3rem;
        font-weight: bold;
    }
    .score-poor {
        color: #dc3545;
        font-size: 3rem;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = None
if 'resume_uploaded' not in st.session_state:
    st.session_state.resume_uploaded = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'chat_session_id' not in st.session_state:
    st.session_state.chat_session_id = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'current_report' not in st.session_state:
    st.session_state.current_report = None

# Sidebar navigation
st.sidebar.title("🎯 Resume Coach AI")
st.sidebar.markdown("---")

# Navigation menu
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📤 Upload Resume", "📊 Analysis", "💬 Chat Coach"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Quick Guide")
st.sidebar.markdown("""
1. **Upload** your resume (PDF)
2. **Paste** the job description
3. **Get** AI coaching analysis
4. **Chat** for personalized advice
""")

st.sidebar.markdown("---")

# Session status
if st.session_state.session_id:
    st.sidebar.success("✅ Session Active")
    if st.session_state.resume_uploaded:
        st.sidebar.info("📄 Resume Uploaded")
    if st.session_state.analysis_complete:
        st.sidebar.info("📊 Analysis Complete")
    if st.session_state.chat_session_id:
        st.sidebar.info("💬 Chat Active")
else:
    st.sidebar.warning("⚠️ No Active Session")

# Check API health
try:
    health_response = requests.get(f"{API_BASE_URL}/api/health", timeout=2)
    if health_response.status_code == 200:
        st.sidebar.success("🟢 API Connected")
    else:
        st.sidebar.error("🔴 API Error")
except:
    st.sidebar.error("🔴 API Offline")
    st.sidebar.caption(f"Expected at: {API_BASE_URL}")

# Page routing
if page == "🏠 Home":
    # Home Page
    st.markdown('<div class="main-header">📄 Resume Coach AI</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Welcome to Your AI Career Coach!</h3>
        <p>Get personalized feedback on your resume and job match in minutes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍 AI-Powered Analysis")
        st.write("Advanced language models analyze your resume against job requirements")
        st.write("✓ Skill gap identification")
        st.write("✓ Strength highlighting")
        st.write("✓ Fit score calculation")
    
    with col2:
        st.markdown("### 💡 Actionable Advice")
        st.write("Get specific, prioritized recommendations")
        st.write("✓ Resume optimization tips")
        st.write("✓ Interview preparation")
        st.write("✓ Timeline suggestions")
    
    with col3:
        st.markdown("### 💬 Interactive Chat")
        st.write("Ask follow-up questions to your AI career coach")
        st.write("✓ Personalized guidance")
        st.write("✓ Context-aware responses")
        st.write("✓ Unlimited questions")
    
    st.markdown("---")
    
    st.markdown("### 🚀 Get Started")
    st.info("👈 Use the sidebar to navigate to **Upload Resume** and begin your coaching session!")
    
    # Feature showcase
    st.markdown("### ✨ Key Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        **📊 Comprehensive Analysis**
        - Overall fit score (0-100)
        - Detailed skill gap analysis
        - Strength identification with evidence
        - Prioritized recommendations
        
        **⚡ Two Analysis Modes**
        - Single-step: Fast, comprehensive report
        - Multi-step: Detailed, specialized analysis
        """)
    
    with features_col2:
        st.markdown("""
        **🎯 Personalized Coaching**
        - Resume-specific feedback
        - Job-tailored recommendations
        - Experience-level appropriate advice
        
        **🔒 Privacy First**
        - No data storage
        - Session-based processing
        - Secure API communication
        """)
    
    st.markdown("---")
    st.markdown("### 📈 Success Stories")
    
    testimonial_col1, testimonial_col2, testimonial_col3 = st.columns(3)
    
    with testimonial_col1:
        st.markdown("""
        > *"Resume Coach helped me identify 5 key skills I was missing for my dream job. 
        > Got the interview in 2 weeks!"*
        
        **- Sarah J., Software Engineer**
        """)
    
    with testimonial_col2:
        st.markdown("""
        > *"The AI coaching was spot-on. The recommendations were actionable and helped me 
        > stand out from other candidates."*
        
        **- Mike T., Data Scientist**
        """)
    
    with testimonial_col3:
        st.markdown("""
        > *"Love the chat feature! Being able to ask follow-up questions made all the difference 
        > in my interview prep."*
        
        **- Lisa K., Product Manager**
        """)

elif page == "📤 Upload Resume":
    from frontend.pages import upload_page
    upload_page.render()

elif page == "📊 Analysis":
    from frontend.pages import analysis_page
    analysis_page.render()

elif page == "💬 Chat Coach":
    from frontend.pages import chat_page
    chat_page.render()
