"""
Upload Resume Page

Handles resume upload and job description input.
"""
import streamlit as st
import requests
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def render():
    """Render the upload resume page."""
    st.markdown('<div class="main-header">📤 Upload Your Resume</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>📋 Step 1: Upload Resume & Job Description</h4>
        <p>Upload your resume (PDF format) and paste the job description you're targeting.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📄 Resume Upload")
        
        uploaded_file = st.file_uploader(
            "Choose your resume PDF",
            type=['pdf'],
            help="Upload your resume in PDF format"
        )
        
        if uploaded_file is not None:
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"📊 File size: {uploaded_file.size / 1024:.1f} KB")
            
            if st.button("🚀 Parse Resume", type="primary"):
                with st.spinner("🔄 Parsing your resume..."):
                    try:
                        # Upload resume to API
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                        response = requests.post(
                            f"{API_BASE_URL}/api/upload-resume",
                            files=files,
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Store session ID
                            st.session_state.session_id = data['session_id']
                            st.session_state.resume_uploaded = True
                            
                            st.markdown('<div class="success-box">', unsafe_allow_html=True)
                            st.markdown("### ✅ Resume Parsed Successfully!")
                            
                            # Display parsed contact info
                            if data.get('contact_info'):
                                contact = data['contact_info']
                                st.markdown("**Contact Information:**")
                                if contact.get('name'):
                                    st.write(f"👤 Name: {contact['name']}")
                                if contact.get('email'):
                                    st.write(f"📧 Email: {contact['email']}")
                                if contact.get('phone'):
                                    st.write(f"📱 Phone: {contact['phone']}")
                                if contact.get('linkedin'):
                                    st.write(f"🔗 LinkedIn: {contact['linkedin']}")
                            
                            # Display sections found
                            if data.get('sections_found'):
                                st.markdown("**Sections Detected:**")
                                sections = ", ".join(data['sections_found'])
                                st.write(f"📑 {sections}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            st.info("👉 Now paste the job description in the right panel and click 'Generate Analysis'")
                            
                        else:
                            st.error(f"❌ Error: {response.json().get('detail', 'Failed to parse resume')}")
                    
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to API. Make sure the backend server is running!")
                        st.code(f"Expected API at: {API_BASE_URL}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.info("📥 Please upload your resume PDF to begin")
    
    with col2:
        st.markdown("### 💼 Job Description")
        
        job_description = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="""Senior Python Developer at TechCorp

Location: San Francisco, CA
Type: Full-time

ABOUT THE ROLE
We are seeking an experienced Python developer...

RESPONSIBILITIES
- Design and develop backend services
- Write clean, maintainable code
- Collaborate with teams

REQUIREMENTS
- 5+ years of Python experience
- Strong knowledge of Django/Flask
- Experience with AWS
...""",
            help="Copy and paste the complete job description"
        )
        
        st.markdown("---")
        
        # Analysis options
        st.markdown("### ⚙️ Analysis Options")
        
        use_multi_step = st.checkbox(
            "Use Multi-Step Analysis (More Detailed)",
            value=False,
            help="Multi-step provides more detailed analysis but takes longer"
        )
        
        if use_multi_step:
            st.info("""
            **Multi-Step Analysis:**
            - Fit Assessment
            - Gap Analysis
            - Strength Analysis
            - Resume Optimization
            - Interview Preparation
            
            ⏱️ Takes 30-60 seconds
            """)
        else:
            st.info("""
            **Single-Step Analysis:**
            - Comprehensive report in one go
            - Faster processing
            
            ⏱️ Takes 10-30 seconds
            """)
    
    # Generate Analysis Button
    st.markdown("---")
    
    if not st.session_state.resume_uploaded:
        st.warning("⚠️ Please upload and parse your resume first")
    elif not job_description or len(job_description) < 50:
        st.warning("⚠️ Please paste a job description (at least 50 characters)")
    else:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🎯 Generate AI Coaching Analysis", type="primary"):
                with st.spinner("🤖 AI is analyzing your resume... This may take 30-60 seconds..."):
                    try:
                        # Call analysis API
                        response = requests.post(
                            f"{API_BASE_URL}/api/analyze",
                            data={
                                'session_id': st.session_state.session_id,
                                'job_description': job_description,
                                'use_multi_step': use_multi_step
                            },
                            timeout=120
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.current_report = data
                            st.session_state.analysis_complete = True
                            
                            st.success("✅ Analysis Complete!")
                            st.balloons()
                            st.info("👉 Go to the **Analysis** page to view your results!")
                            
                        elif response.status_code == 404:
                            st.error("❌ Session not found. Please upload your resume again.")
                            st.session_state.resume_uploaded = False
                            st.session_state.session_id = None
                        else:
                            error_detail = response.json().get('detail', 'Analysis failed')
                            st.error(f"❌ Error: {error_detail}")
                    
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timed out. The analysis is taking longer than expected. Please try again.")
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to API. Make sure the backend server is running!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Tips section
    st.markdown("---")
    st.markdown("### 💡 Tips for Best Results")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **Resume Tips:**
        - ✓ Use a standard PDF format
        - ✓ Include contact information at the top
        - ✓ Clear section headers (Experience, Education, Skills)
        - ✓ List specific technologies and tools
        - ✓ Quantify achievements when possible
        """)
    
    with tips_col2:
        st.markdown("""
        **Job Description Tips:**
        - ✓ Copy the complete job posting
        - ✓ Include all sections (requirements, responsibilities)
        - ✓ Keep original formatting if possible
        - ✓ Include both required and preferred qualifications
        - ✓ Don't edit or summarize the description
        """)
