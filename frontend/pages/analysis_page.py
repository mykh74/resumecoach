"""
Analysis Results Page

Displays the AI coaching analysis results.
"""
import streamlit as st
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def get_score_class(score):
    """Get CSS class based on score."""
    if score >= 80:
        return "score-excellent"
    elif score >= 65:
        return "score-good"
    elif score >= 50:
        return "score-fair"
    else:
        return "score-poor"


def get_score_label(score):
    """Get label based on score."""
    if score >= 80:
        return "Excellent Match! 🎉"
    elif score >= 65:
        return "Good Match 👍"
    elif score >= 50:
        return "Fair Match 🤔"
    else:
        return "Needs Improvement 💪"


def get_severity_icon(severity):
    """Get icon for severity level."""
    severity_lower = severity.lower()
    if severity_lower == "high" or severity_lower == "critical":
        return "🔴"
    elif severity_lower == "medium":
        return "🟡"
    else:
        return "🟢"


def get_priority_icon(priority):
    """Get icon for priority level."""
    priority_lower = priority.lower()
    if priority_lower == "high":
        return "🔥"
    elif priority_lower == "medium":
        return "⚡"
    else:
        return "💡"


def render():
    """Render the analysis results page."""
    st.markdown('<div class="main-header">📊 AI Coaching Analysis</div>', unsafe_allow_html=True)
    
    # Check if analysis is complete
    if not st.session_state.analysis_complete or not st.session_state.current_report:
        st.markdown("""
        <div class="warning-box">
            <h3>⚠️ No Analysis Available</h3>
            <p>Please upload your resume and generate an analysis first.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("👉 Go to **Upload Resume** page to get started!")
        return
    
    report = st.session_state.current_report
    
    # Overall Fit Score
    st.markdown("### 🎯 Overall Fit Score")
    
    score = report['overall_fit_score']
    score_class = get_score_class(score)
    score_label = get_score_label(score)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="{score_class}">{score}/100</div>
            <h3>{score_label}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Summary
    st.markdown("### 📝 Executive Summary")
    st.markdown(f"""
    <div class="info-box">
        {report['summary']}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create two columns for gaps and strengths
    col_left, col_right = st.columns(2)
    
    # Gaps Analysis
    with col_left:
        st.markdown("### ❌ Skill Gaps & Areas for Improvement")
        
        if report['gaps']:
            for i, gap in enumerate(report['gaps'], 1):
                severity_icon = get_severity_icon(gap['severity'])
                
                with st.expander(f"{severity_icon} {gap['skill_area']} - {gap['severity'].title()} Priority", expanded=(i <= 3)):
                    st.markdown(f"**Impact:** {gap['impact']}")
                    st.markdown(f"**Suggestion:** {gap['suggestion']}")
        else:
            st.success("✅ No major gaps identified! Your resume looks well-aligned with the job.")
    
    # Strengths Analysis
    with col_right:
        st.markdown("### ✅ Key Strengths")
        
        if report['strengths']:
            for i, strength in enumerate(report['strengths'], 1):
                relevance_icon = "🌟" if strength['relevance'].lower() == "high" else "⭐" if strength['relevance'].lower() == "medium" else "✨"
                
                with st.expander(f"{relevance_icon} {strength['skill_area']} - {strength['relevance'].title()} Relevance", expanded=(i <= 3)):
                    st.markdown(f"**Evidence:** {strength['evidence']}")
                    st.markdown(f"**How to Highlight:** {strength['how_to_highlight']}")
        else:
            st.info("💡 Consider highlighting your relevant experience more prominently.")
    
    st.markdown("---")
    
    # Actionable Recommendations
    st.markdown("### 💡 Actionable Recommendations")
    
    if report['recommendations']:
        # Group recommendations by priority
        high_priority = [r for r in report['recommendations'] if r['priority'].lower() == 'high']
        medium_priority = [r for r in report['recommendations'] if r['priority'].lower() == 'medium']
        low_priority = [r for r in report['recommendations'] if r['priority'].lower() == 'low']
        
        # High priority first
        if high_priority:
            st.markdown("#### 🔥 High Priority")
            for rec in high_priority:
                priority_icon = get_priority_icon(rec['priority'])
                st.markdown(f"""
                <div class="warning-box">
                    <strong>{priority_icon} {rec['action']}</strong><br>
                    {f"<em>Timeline: {rec['timeline']}</em>" if rec.get('timeline') else ""}
                </div>
                """, unsafe_allow_html=True)
        
        # Medium priority
        if medium_priority:
            st.markdown("#### ⚡ Medium Priority")
            for rec in medium_priority:
                priority_icon = get_priority_icon(rec['priority'])
                st.markdown(f"""
                <div class="info-box">
                    <strong>{priority_icon} {rec['action']}</strong><br>
                    {f"<em>Timeline: {rec['timeline']}</em>" if rec.get('timeline') else ""}
                </div>
                """, unsafe_allow_html=True)
        
        # Low priority
        if low_priority:
            with st.expander("💡 Additional Suggestions (Low Priority)"):
                for rec in low_priority:
                    priority_icon = get_priority_icon(rec['priority'])
                    st.markdown(f"- {priority_icon} {rec['action']}")
                    if rec.get('timeline'):
                        st.caption(f"Timeline: {rec['timeline']}")
    else:
        st.info("No specific recommendations at this time.")
    
    st.markdown("---")
    
    # Analysis Details
    with st.expander("📋 Analysis Details"):
        st.write(f"**Analysis Type:** {report.get('analysis_type', 'N/A')}")
        st.write(f"**Session ID:** {report.get('session_id', 'N/A')}")
        st.write(f"**Generated:** {report.get('created_at', 'N/A')}")
    
    # Action buttons
    st.markdown("---")
    st.markdown("### 🚀 Next Steps")
    
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("💬 Chat with AI Coach", type="primary"):
            st.info("👉 Go to the **Chat Coach** page to ask follow-up questions!")
    
    with action_col2:
        if st.button("🔄 New Analysis"):
            st.session_state.analysis_complete = False
            st.session_state.current_report = None
            st.session_state.resume_uploaded = False
            st.session_state.session_id = None
            st.success("✅ Session reset! You can upload a new resume.")
            st.rerun()
    
    with action_col3:
        # Download report as text
        report_text = f"""RESUME COACHING ANALYSIS REPORT
{'=' * 50}

Overall Fit Score: {score}/100
{score_label}

SUMMARY
{'-' * 50}
{report['summary']}

SKILL GAPS
{'-' * 50}
"""
        for gap in report['gaps']:
            report_text += f"\n• {gap['skill_area']} ({gap['severity']})\n"
            report_text += f"  Impact: {gap['impact']}\n"
            report_text += f"  Suggestion: {gap['suggestion']}\n"

        report_text += f"\nKEY STRENGTHS\n{'-' * 50}\n"
        for strength in report['strengths']:
            report_text += f"\n• {strength['skill_area']} ({strength['relevance']})\n"
            report_text += f"  Evidence: {strength['evidence']}\n"
            report_text += f"  How to Highlight: {strength['how_to_highlight']}\n"

        report_text += f"\nRECOMMENDATIONS\n{'-' * 50}\n"
        for rec in report['recommendations']:
            report_text += f"\n[{rec['priority'].upper()}] {rec['action']}\n"
            if rec.get('timeline'):
                report_text += f"Timeline: {rec['timeline']}\n"
        
        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name="resume_coaching_report.txt",
            mime="text/plain"
        )
    
    # Tips for improvement
    st.markdown("---")
    st.markdown("### 📚 Additional Resources")
    
    resources_col1, resources_col2 = st.columns(2)
    
    with resources_col1:
        st.markdown("""
        **Resume Improvement:**
        - Focus on high-priority gaps first
        - Quantify your achievements with numbers
        - Use action verbs (led, developed, improved)
        - Tailor your resume for this specific job
        - Keep formatting clean and consistent
        """)
    
    with resources_col2:
        st.markdown("""
        **Interview Preparation:**
        - Prepare examples for your strengths
        - Have a plan to address skill gaps
        - Practice explaining your experience
        - Research the company thoroughly
        - Prepare questions about the role
        """)
