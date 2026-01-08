# Resume Coach - Streamlit Frontend

## Overview
Interactive web interface for AI-powered resume coaching built with Streamlit.

## Features

### 🏠 Home Page
- Welcome screen with feature showcase
- Success stories and testimonials
- Quick guide for getting started

### 📤 Upload Resume Page
- PDF resume upload with drag-and-drop
- Resume parsing and validation
- Job description text input
- Analysis options (single-step vs multi-step)
- Real-time parsing feedback

### 📊 Analysis Page
- Overall fit score (0-100) with visual indicator
- Executive summary
- Skill gaps with severity levels
- Key strengths with evidence
- Prioritized actionable recommendations
- Download report as text file

### 💬 Chat Coach Page
- Interactive AI career coach
- Context-aware responses
- Suggested questions for quick start
- Chat history management
- Download conversation history

## Running the Frontend

### Option 1: Standalone (Frontend Only)
```bash
cd /Users/michaelkuzmyn/projects/ik/ResumeCoach
source venv/bin/activate
streamlit run frontend/streamlit_app.py
```

The frontend will be available at: http://localhost:8501

**Note:** The backend API must be running separately at http://localhost:8000

### Option 2: Full Application (Backend + Frontend)
```bash
cd /Users/michaelkuzmyn/projects/ik/ResumeCoach
./run_app.sh
```

This script will:
1. Start the backend API on port 8000
2. Start the Streamlit frontend on port 8501
3. Handle graceful shutdown with Ctrl+C

## Environment Variables

Set these in your environment or `.env` file:

```bash
API_BASE_URL=http://localhost:8000  # Backend API URL (default)
```

## Pages Structure

```
frontend/
├── streamlit_app.py          # Main application entry point
└── pages/
    ├── __init__.py
    ├── upload_page.py         # Resume upload & job description
    ├── analysis_page.py       # Analysis results display
    └── chat_page.py           # AI coach chat interface
```

## Navigation Flow

1. **Home** → Introduction and features
2. **Upload Resume** → Upload PDF + paste job description → Generate analysis
3. **Analysis** → View results, gaps, strengths, recommendations
4. **Chat Coach** → Ask follow-up questions, get personalized advice

## Session Management

The frontend uses Streamlit's session state to maintain:
- `session_id`: Backend session identifier
- `resume_uploaded`: Resume upload status
- `analysis_complete`: Analysis completion status
- `chat_session_id`: Chat session identifier
- `chat_messages`: Conversation history
- `current_report`: Latest analysis report

## UI Components

### Custom CSS Styling
- Color-coded score indicators (excellent/good/fair/poor)
- Styled info/success/warning/error boxes
- Responsive layout with columns
- Card-based metric displays

### Interactive Elements
- File uploader with validation
- Text areas for job descriptions
- Expandable sections for detailed information
- Download buttons for reports and chat history
- Suggested question buttons in chat

### Visual Feedback
- Spinners for async operations
- Progress indicators
- Success/error messages
- Status indicators in sidebar
- Balloons animation on success

## API Integration

The frontend communicates with the backend via REST API:

```python
import requests

# Upload resume
response = requests.post(
    f"{API_BASE_URL}/api/upload-resume",
    files={'file': (filename, file_bytes, 'application/pdf')}
)

# Generate analysis
response = requests.post(
    f"{API_BASE_URL}/api/analyze",
    data={
        'session_id': session_id,
        'job_description': job_text,
        'use_multi_step': False
    }
)

# Chat
response = requests.post(
    f"{API_BASE_URL}/api/chat/sessions/{chat_id}/messages",
    json={'message': user_message}
)
```

## Error Handling

- Connection errors: Alerts user if backend is offline
- Validation errors: Shows field-specific error messages
- Timeout handling: 120s for analysis, 60s for chat
- Session expiry: Prompts user to restart workflow

## User Experience Features

### Smart Defaults
- Single-step analysis by default (faster)
- Multi-step available for detailed reports
- Auto-scroll to important content

### Helpful Guidance
- Tips on each page
- Example questions in chat
- Inline help text for forms
- Status indicators in sidebar

### Data Export
- Download analysis report as text
- Download chat history as text
- Copy session IDs for debugging

## Responsive Design

The interface adapts to different screen sizes:
- Desktop: Full 3-column layout
- Tablet: 2-column layout
- Mobile: Single-column stacked layout

## Testing the Frontend

### Manual Testing Checklist

1. **Upload Page**
   - [ ] Upload PDF resume
   - [ ] See parsed contact info
   - [ ] Paste job description
   - [ ] Toggle multi-step option
   - [ ] Generate analysis

2. **Analysis Page**
   - [ ] See fit score
   - [ ] Read summary
   - [ ] Expand gap details
   - [ ] Expand strength details
   - [ ] View recommendations
   - [ ] Download report

3. **Chat Page**
   - [ ] Initialize chat session
   - [ ] Send custom message
   - [ ] Click suggested questions
   - [ ] View conversation history
   - [ ] Download chat history
   - [ ] Clear chat

4. **Navigation**
   - [ ] Switch between pages
   - [ ] Check sidebar status
   - [ ] Verify API health indicator

## Dependencies

Main Streamlit dependencies:
- `streamlit>=1.52.2` - Web framework
- `requests>=2.31.0` - HTTP client for API calls

See `requirements-core.txt` for complete list.

## Customization

### Changing Colors
Edit the custom CSS in `streamlit_app.py`:
```python
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;  /* Change header color */
    }
</style>
""", unsafe_allow_html=True)
```

### Adding New Pages
1. Create new file in `frontend/pages/`
2. Implement `render()` function
3. Add navigation option in `streamlit_app.py`
4. Import and call the render function

### Modifying Analysis Display
Edit `analysis_page.py`:
- Change score thresholds in `get_score_class()`
- Modify severity icons in `get_severity_icon()`
- Adjust layout columns and sections

## Production Considerations

### Performance
- Cache API responses where appropriate
- Lazy load large data
- Optimize image sizes
- Minimize API calls

### Security
- Validate all user inputs
- Sanitize file uploads
- Use HTTPS in production
- Set proper CORS headers

### Deployment
- Use `streamlit run` with production settings
- Configure server.port and server.address
- Set up reverse proxy (nginx)
- Enable authentication if needed

## Troubleshooting

### Backend Not Connecting
- Check if API is running: `curl http://localhost:8000/api/health`
- Verify API_BASE_URL in environment
- Check firewall/port settings

### File Upload Fails
- Ensure file is PDF format
- Check file size (max ~10MB)
- Verify /tmp directory is writable
- Check backend logs for errors

### Chat Not Working
- Ensure analysis is complete first
- Check chat session initialization
- Verify timeout settings (60s)
- Review backend LLM service status

### Page Not Refreshing
- Use `st.rerun()` after state changes
- Check session state management
- Clear browser cache if needed

## Future Enhancements

- [ ] Add authentication/user accounts
- [ ] Store analysis history in database
- [ ] Add resume comparison feature
- [ ] Implement real-time collaboration
- [ ] Add data visualization charts
- [ ] Support multiple file formats (DOCX, TXT)
- [ ] Add export to PDF with formatting
- [ ] Implement progress tracking over time

---

**Built with:** Streamlit 1.52.2  
**Requires:** Backend API running on port 8000  
**Access:** http://localhost:8501
