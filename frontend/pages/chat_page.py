"""
Chat with AI Coach Page

Interactive chat interface for personalized coaching.
"""
import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def render():
    """Render the chat page."""
    st.markdown('<div class="main-header">💬 Chat with Your AI Career Coach</div>', unsafe_allow_html=True)
    
    # Check prerequisites
    if not st.session_state.analysis_complete:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ Analysis Required First</h3>
            <p>Please complete a resume analysis before chatting with the AI coach.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("👉 Go to **Upload Resume** page to get started!")
        return
    
    st.markdown("""
    <div class="info-box">
        <h4>💡 Ask Your AI Career Coach Anything!</h4>
        <p>Get personalized advice about your resume, the job, or your career strategy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create chat session if not exists
    if not st.session_state.chat_session_id:
        with st.spinner("🔄 Initializing chat session..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/chat/sessions",
                    data={'session_id': st.session_state.session_id},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.chat_session_id = data['chat_session_id']
                    st.success("✅ Chat session initialized!")
                else:
                    st.error(f"❌ Failed to create chat session: {response.json().get('detail', 'Unknown error')}")
                    return
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                return
    
    # Display chat history
    st.markdown("### 💬 Conversation")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        if not st.session_state.chat_messages:
            st.info("👋 Hello! I'm your AI career coach. Ask me anything about your resume, the job requirements, or how to improve your candidacy!")
        else:
            for message in st.session_state.chat_messages:
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                        <strong>👤 You:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: #f5f5f5; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                        <strong>🤖 AI Coach:</strong><br>
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
    
    # Message input
    st.markdown("---")
    
    # Suggested questions
    st.markdown("### 💡 Suggested Questions")
    
    suggestions_col1, suggestions_col2, suggestions_col3 = st.columns(3)
    
    with suggestions_col1:
        if st.button("🎯 Top skills to focus on?"):
            user_message = "What are the top 3 skills I should focus on improving for this role?"
            send_message(user_message)
            st.rerun()
        
        if st.button("📝 Resume improvements?"):
            user_message = "What specific improvements should I make to my resume?"
            send_message(user_message)
            st.rerun()
    
    with suggestions_col2:
        if st.button("💼 Interview preparation?"):
            user_message = "How should I prepare for the interview for this position?"
            send_message(user_message)
            st.rerun()
        
        if st.button("⏱️ Timeline for improvement?"):
            user_message = "What's a realistic timeline to address the gaps you identified?"
            send_message(user_message)
            st.rerun()
    
    with suggestions_col3:
        if st.button("🎓 Learning resources?"):
            user_message = "What learning resources or courses would you recommend for the skill gaps?"
            send_message(user_message)
            st.rerun()
        
        if st.button("💪 Highlighting strengths?"):
            user_message = "How can I better highlight my key strengths in interviews?"
            send_message(user_message)
            st.rerun()
    
    st.markdown("---")
    
    # Custom message input
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your question:",
            placeholder="Type your question here... (e.g., 'How can I demonstrate my Python skills better?')",
            height=100,
            key="user_input"
        )
        
        submit_col1, submit_col2, submit_col3 = st.columns([1, 1, 1])
        with submit_col2:
            submit_button = st.form_submit_button("Send 📤", type="primary")
        
        if submit_button and user_input.strip():
            send_message(user_input.strip())
            st.rerun()
    
    # Chat controls
    st.markdown("---")
    
    control_col1, control_col2 = st.columns(2)
    
    with control_col1:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_messages = []
            st.session_state.chat_session_id = None
            st.success("✅ Chat history cleared!")
            st.rerun()
    
    with control_col2:
        if st.button("📥 Download Chat History"):
            chat_text = "CHAT HISTORY - AI CAREER COACH\n"
            chat_text += "=" * 50 + "\n\n"
            
            for message in st.session_state.chat_messages:
                if message['role'] == 'user':
                    chat_text += f"YOU: {message['content']}\n\n"
                else:
                    chat_text += f"AI COACH: {message['content']}\n\n"
                chat_text += "-" * 50 + "\n\n"
            
            st.download_button(
                label="📥 Download Chat",
                data=chat_text,
                file_name="chat_history.txt",
                mime="text/plain",
                key="download_chat"
            )
    
    # Tips
    st.markdown("---")
    st.markdown("### 💡 Chat Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **Getting the Most from Your Coach:**
        - ✓ Ask specific, detailed questions
        - ✓ Reference particular gaps or strengths
        - ✓ Ask for examples and action items
        - ✓ Request timeline and prioritization help
        - ✓ Follow up on previous answers
        """)
    
    with tips_col2:
        st.markdown("""
        **Example Questions:**
        - "How can I gain Kubernetes experience quickly?"
        - "What projects should I add to my resume?"
        - "How do I explain my career gap?"
        - "What certifications would help most?"
        - "How should I tailor my cover letter?"
        """)


def send_message(message: str):
    """Send a message to the AI coach."""
    try:
        # Add user message to display immediately
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': message
        })
        
        # Send to API
        with st.spinner("🤖 AI Coach is thinking..."):
            response = requests.post(
                f"{API_BASE_URL}/api/chat/sessions/{st.session_state.chat_session_id}/messages",
                json={'message': message},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Add AI response
                st.session_state.chat_messages.append({
                    'role': 'assistant',
                    'content': data['response']
                })
            else:
                error_msg = response.json().get('detail', 'Failed to get response')
                st.error(f"❌ Error: {error_msg}")
                # Remove the user message since it failed
                st.session_state.chat_messages.pop()
    
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
        # Remove the user message since it failed
        if st.session_state.chat_messages and st.session_state.chat_messages[-1]['role'] == 'user':
            st.session_state.chat_messages.pop()
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        # Remove the user message since it failed
        if st.session_state.chat_messages and st.session_state.chat_messages[-1]['role'] == 'user':
            st.session_state.chat_messages.pop()
