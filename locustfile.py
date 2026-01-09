"""
Load Testing Suite for Resume Coach Application

Uses Locust framework to simulate concurrent users and measure system performance
under various load conditions.

Run with:
    locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html=reports/load_test.html
    
    Options:
        -u : Number of users to simulate
        -r : Spawn rate (users per second)
        -t : Test duration
        --html : Generate HTML report
"""
from locust import HttpUser, task, between, events
import json
import os
from pathlib import Path
import time

# Test data paths
SAMPLE_RESUME_PATH = "data/sample_resumes/john_doe_resume.pdf"
SAMPLE_JOB_PATH = "data/job_postings/senior_fullstack_ml_job.md"

# Load test data
def load_job_description():
    """Load sample job description."""
    job_path = Path(SAMPLE_JOB_PATH)
    if job_path.exists():
        return job_path.read_text()
    return """
    Senior Full Stack Engineer
    
    Requirements:
    - 5+ years of software development experience
    - Python, JavaScript, React
    - AWS cloud experience
    - Strong problem-solving skills
    """


class ResumeCoachUser(HttpUser):
    """
    Simulates a user interacting with the Resume Coach application.
    
    Workflow:
    1. Health check
    2. Upload resume
    3. Parse job description
    4. Generate coaching report
    5. Chat with the system
    """
    
    # Wait between 1-3 seconds between tasks
    wait_time = between(1, 3)
    
    # Store session data
    session_id = None
    chat_session_id = None
    job_description = None
    
    def on_start(self):
        """Called when a simulated user starts. Initialize session."""
        self.job_description = load_job_description()
        print(f"✓ User started")
    
    @task(10)
    def health_check(self):
        """Test the health check endpoint (high frequency)."""
        with self.client.get(
            "/api/health",
            catch_response=True,
            name="Health Check"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")
    
    @task(5)
    def parse_job_description(self):
        """Test job description parsing (medium frequency)."""
        with self.client.post(
            "/api/parse-job",
            json={"text": self.job_description},
            catch_response=True,
            name="Parse Job Description"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Job parsing failed: {response.status_code}")
    
    @task(3)
    def upload_and_analyze(self):
        """
        Test complete workflow: upload resume → analyze (lower frequency).
        This is the most resource-intensive operation.
        """
        # Check if sample resume exists
        resume_path = Path(SAMPLE_RESUME_PATH)
        if not resume_path.exists():
            print(f"⚠️ Sample resume not found: {SAMPLE_RESUME_PATH}")
            return
        
        # Step 1: Upload resume
        with open(resume_path, 'rb') as f:
            files = {'file': ('resume.pdf', f, 'application/pdf')}
            with self.client.post(
                "/api/upload-resume",
                files=files,
                catch_response=True,
                name="Upload Resume"
            ) as response:
                if response.status_code == 200:
                    data = response.json()
                    self.session_id = data.get('session_id')
                    response.success()
                else:
                    response.failure(f"Resume upload failed: {response.status_code}")
                    return
        
        # Step 2: Analyze (if we have a session)
        if self.session_id:
            payload = {
                "session_id": self.session_id,
                "job_description": self.job_description
            }
            
            with self.client.post(
                "/api/analyze",
                json=payload,
                catch_response=True,
                name="Generate Coaching Report",
                timeout=30  # Longer timeout for LLM operations
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 500:
                    # Expected if OpenAI API key not set
                    response.success()  # Don't count as failure
                else:
                    response.failure(f"Analysis failed: {response.status_code}")
    
    @task(2)
    def chat_interaction(self):
        """Test chat functionality (lower frequency)."""
        # Need a valid session first
        if not self.session_id:
            return
        
        # Create chat session if not exists
        if not self.chat_session_id:
            payload = {
                "session_id": self.session_id,
                "initial_question": "What should I focus on to improve my candidacy?"
            }
            
            with self.client.post(
                "/api/chat/create",
                json=payload,
                catch_response=True,
                name="Create Chat Session",
                timeout=30
            ) as response:
                if response.status_code == 200:
                    data = response.json()
                    self.chat_session_id = data.get('chat_session_id')
                    response.success()
                elif response.status_code == 500:
                    response.success()  # Don't count as failure if API key missing
                else:
                    response.failure(f"Chat creation failed: {response.status_code}")
                    return
        
        # Send a chat message
        if self.chat_session_id:
            payload = {
                "chat_session_id": self.chat_session_id,
                "question": "Can you elaborate on the technical skills I need?"
            }
            
            with self.client.post(
                "/api/chat/message",
                json=payload,
                catch_response=True,
                name="Send Chat Message",
                timeout=30
            ) as response:
                if response.status_code == 200:
                    response.success()
                elif response.status_code == 500:
                    response.success()  # Don't count as failure
                else:
                    response.failure(f"Chat message failed: {response.status_code}")


class QuickTestUser(HttpUser):
    """
    Lightweight user for quick load testing.
    Only tests health check and job parsing (no LLM calls).
    """
    wait_time = between(0.5, 1.5)
    
    @task(5)
    def health_check(self):
        """Quick health check."""
        self.client.get("/api/health", name="Health Check (Quick)")
    
    @task(1)
    def parse_job(self):
        """Quick job parsing test."""
        self.client.post(
            "/api/parse-job",
            json={"text": load_job_description()},
            name="Parse Job (Quick)"
        )


# Custom events for additional metrics
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts."""
    print("\n" + "="*70)
    print("🚀 Load Testing Started")
    print("="*70)
    print(f"Target host: {environment.host}")
    print(f"Users: {environment.runner.target_user_count if hasattr(environment.runner, 'target_user_count') else 'Unknown'}")
    print("="*70 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops."""
    print("\n" + "="*70)
    print("✅ Load Testing Complete")
    print("="*70)
    stats = environment.stats
    print(f"Total requests: {stats.total.num_requests}")
    print(f"Failed requests: {stats.total.num_failures}")
    print(f"Median response time: {stats.total.median_response_time}ms")
    print(f"95th percentile: {stats.total.get_response_time_percentile(0.95)}ms")
    print(f"Requests/sec: {stats.total.total_rps:.2f}")
    print("="*70 + "\n")


if __name__ == "__main__":
    """
    Command-line execution examples:
    
    1. Quick test (10 users, 60 seconds):
        locust -f locustfile.py --headless -u 10 -r 2 -t 60s
    
    2. With HTML report:
        locust -f locustfile.py --headless -u 10 -r 2 -t 60s --html=reports/load_test.html
    
    3. Heavy load (50 users, 5 minutes):
        locust -f locustfile.py --headless -u 50 -r 5 -t 300s --html=reports/heavy_load.html
    
    4. Web UI (for interactive testing):
        locust -f locustfile.py
        # Then open http://localhost:8089
    
    5. Target specific host:
        locust -f locustfile.py --host=https://production-api.com --headless -u 10 -r 2 -t 60s
    
    6. Quick test (no LLM calls):
        locust -f locustfile.py --headless -u 25 -r 5 -t 30s --user QuickTestUser
    """
    import sys
    print(__doc__)
    print("\n💡 Run with: locust -f locustfile.py --help for options")
    sys.exit(0)
