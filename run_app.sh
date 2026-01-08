#!/bin/bash
# Start Resume Coach Application (Backend + Frontend)

echo "🚀 Starting Resume Coach Application..."
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Set PYTHONPATH
export PYTHONPATH=/Users/michaelkuzmyn/projects/ik/ResumeCoach

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Backend API already running on port 8000"
else
    echo "🔧 Starting Backend API on port 8000..."
    python -m backend.api.main > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo "   Backend PID: $BACKEND_PID"
    sleep 3
fi

# Start Streamlit frontend
echo "🎨 Starting Streamlit Frontend on port 8501..."
streamlit run frontend/streamlit_app.py --server.port 8501 --server.address localhost

# Cleanup on exit
trap "echo ''; echo '🛑 Shutting down...'; kill $BACKEND_PID 2>/dev/null; exit" INT TERM
