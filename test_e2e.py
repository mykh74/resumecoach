"""
End-to-end testing script for Resume Coach application.
Tests the complete workflow: upload → analyze → chat
"""
import requests
import time
import json
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"
RESUME_PATH = "data/sample_resumes/john_doe_resume.pdf"
JOB_DESCRIPTION_PATH = "data/job_postings/senior_fullstack_ml_job.md"

# Test results tracking
tests_passed = 0
tests_failed = 0
test_results = []

def log_test(test_name, passed, message=""):
    """Log test result."""
    global tests_passed, tests_failed
    status = "✅ PASS" if passed else "❌ FAIL"
    result = f"{status} - {test_name}"
    if message:
        result += f": {message}"
    print(result)
    test_results.append(result)
    if passed:
        tests_passed += 1
    else:
        tests_failed += 1

def test_backend_health():
    """Test 1: Backend health check."""
    print("\n" + "="*70)
    print("TEST 1: Backend Health Check")
    print("="*70)
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            log_test("Backend Health", True, f"Status: {data.get('status')}")
            print(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            log_test("Backend Health", False, f"Status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        log_test("Backend Health", False, "Backend not running on port 8000")
        return False
    except Exception as e:
        log_test("Backend Health", False, str(e))
        return False

def test_upload_resume():
    """Test 2: Resume upload."""
    print("\n" + "="*70)
    print("TEST 2: Resume Upload")
    print("="*70)
    try:
        resume_path = Path(RESUME_PATH)
        if not resume_path.exists():
            log_test("Resume Upload", False, f"Resume file not found: {RESUME_PATH}")
            return None
        
        with open(resume_path, 'rb') as f:
            files = {'file': (resume_path.name, f, 'application/pdf')}
            response = requests.post(
                f"{API_BASE_URL}/api/upload-resume",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            contact_info = data.get('contact_info', {})
            log_test("Resume Upload", True, f"Session ID: {session_id}")
            print(f"Contact Info: {json.dumps(contact_info, indent=2)}")
            print(f"Sections Found: {len(data.get('sections', {}))}")
            return session_id
        else:
            log_test("Resume Upload", False, f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        log_test("Resume Upload", False, str(e))
        return None

def test_single_step_analysis(session_id):
    """Test 3: Single-step analysis."""
    print("\n" + "="*70)
    print("TEST 3: Single-Step Analysis")
    print("="*70)
    try:
        job_path = Path(JOB_DESCRIPTION_PATH)
        if not job_path.exists():
            log_test("Single-Step Analysis", False, f"Job file not found: {JOB_DESCRIPTION_PATH}")
            return None
        
        job_description = job_path.read_text()
        
        payload = {
            'session_id': session_id,
            'job_description': job_description,
            'use_multi_step': False
        }
        
        print("Generating analysis (this may take 10-20 seconds)...")
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            data=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            # Print full response for debugging
            print(f"\nFull API Response Keys: {list(data.keys())}")
            
            # Extract data - API returns flat structure
            report_id = data.get('report_id')
            fit_score = data.get('overall_fit_score', 0)
            summary = data.get('summary', '')
            gaps_count = len(data.get('gaps', []))
            strengths_count = len(data.get('strengths', []))
            recommendations_count = len(data.get('recommendations', []))
            
            log_test("Single-Step Analysis", True, f"Fit Score: {fit_score}/100")
            print(f"\nFit Score: {fit_score}/100")
            print(f"Summary: {summary[:200]}...")
            print(f"Skill Gaps: {gaps_count}")
            print(f"Key Strengths: {strengths_count}")
            print(f"Recommendations: {recommendations_count}")
            
            # Return analysis if we have meaningful data
            if gaps_count > 0 or strengths_count > 0:
                return data
            else:
                print("\n⚠️  Warning: Analysis returned but with no gaps/strengths detected")
                return data  # Still return for chat testing
        else:
            log_test("Single-Step Analysis", False, f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        log_test("Single-Step Analysis", False, str(e))
        return None

def test_chat_session_init(session_id):
    """Test 4: Chat session initialization."""
    print("\n" + "="*70)
    print("TEST 4: Chat Session Initialization")
    print("="*70)
    try:
        payload = {'session_id': session_id}
        response = requests.post(
            f"{API_BASE_URL}/api/chat/sessions",
            data=payload,  # Use data= for form data, not json=
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            chat_session_id = data.get('chat_session_id')
            log_test("Chat Session Init", True, f"Chat Session ID: {chat_session_id}")
            return chat_session_id
        else:
            log_test("Chat Session Init", False, f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        log_test("Chat Session Init", False, str(e))
        return None

def test_chat_message(chat_session_id):
    """Test 5: Send chat message."""
    print("\n" + "="*70)
    print("TEST 5: Chat Message Exchange")
    print("="*70)
    try:
        test_questions = [
            "What are the top 3 skills I should focus on?",
            "How can I improve my resume for this role?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            print(f"\nQuestion {i}: {question}")
            payload = {'message': question}
            response = requests.post(
                f"{API_BASE_URL}/api/chat/sessions/{chat_session_id}/messages",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', '')
                log_test(f"Chat Message {i}", True, f"Response length: {len(answer)} chars")
                print(f"Response: {answer[:300]}...")
            else:
                log_test(f"Chat Message {i}", False, f"Status: {response.status_code}")
                print(f"Response: {response.text}")
            
            time.sleep(1)  # Brief pause between messages
        
        return True
    except Exception as e:
        log_test("Chat Message", False, str(e))
        return False

def test_chat_history(chat_session_id):
    """Test 6: Get chat history."""
    print("\n" + "="*70)
    print("TEST 6: Chat History Retrieval")
    print("="*70)
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/chat/sessions/{chat_session_id}/history",
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            log_test("Chat History", True, f"Messages: {len(messages)}")
            for msg in messages[:3]:  # Show first 3 messages
                print(f"- {msg.get('role')}: {msg.get('content')[:100]}...")
            return True
        else:
            log_test("Chat History", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test("Chat History", False, str(e))
        return False

def print_summary():
    """Print test summary."""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    total_tests = tests_passed + tests_failed
    success_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {tests_passed} ✅")
    print(f"Failed: {tests_failed} ❌")
    print(f"Success Rate: {success_rate:.1f}%\n")
    
    if tests_failed == 0:
        print("🎉 All tests passed! Application is working correctly.")
    else:
        print("⚠️  Some tests failed. Review the results above.")
    
    print("\n" + "="*70)
    print("DETAILED RESULTS")
    print("="*70)
    for result in test_results:
        print(result)

def main():
    """Run all tests."""
    print("="*70)
    print("RESUME COACH - END-TO-END TESTING")
    print("="*70)
    print(f"API Base URL: {API_BASE_URL}")
    print(f"Resume: {RESUME_PATH}")
    print(f"Job Description: {JOB_DESCRIPTION_PATH}")
    
    # Test 1: Health check
    if not test_backend_health():
        print("\n❌ Backend not available. Please start the backend first:")
        print("   python -m backend.api.main")
        return
    
    # Test 2: Upload resume
    session_id = test_upload_resume()
    if not session_id:
        print("\n❌ Resume upload failed. Cannot continue with remaining tests.")
        print_summary()
        return
    
    # Test 3: Generate analysis
    analysis = test_single_step_analysis(session_id)
    if not analysis:
        print("\n⚠️  Analysis generation failed. Skipping chat tests.")
        print_summary()
        return
    
    # Test 4: Initialize chat
    chat_session_id = test_chat_session_init(session_id)
    if not chat_session_id:
        print("\n⚠️  Chat session initialization failed. Skipping chat tests.")
        print_summary()
        return
    
    # Test 5: Send messages
    test_chat_message(chat_session_id)
    
    # Test 6: Get history
    test_chat_history(chat_session_id)
    
    # Print summary
    print_summary()

if __name__ == "__main__":
    main()
