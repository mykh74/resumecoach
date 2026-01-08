#!/usr/bin/env python3
"""
Quick API test script - demonstrates full workflow.
Run this after starting the API server.
"""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint."""
    print("1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_job_parsing():
    """Test job description parsing."""
    print("\n2. Testing job description parsing...")
    
    job_text = """
    Senior Python Developer at TechCorp
    
    Location: San Francisco, CA
    Type: Full-time
    
    RESPONSIBILITIES
    - Design and develop backend services using Python
    - Write clean, maintainable code
    - Collaborate with cross-functional teams
    
    REQUIREMENTS
    - 5+ years of Python development experience
    - Strong knowledge of Django or Flask
    - Experience with AWS and cloud technologies
    - Bachelor's degree in Computer Science
    
    PREFERRED QUALIFICATIONS
    - Experience with React
    - Knowledge of Docker and Kubernetes
    
    BENEFITS
    - Competitive salary $150k-$200k
    - Health insurance
    - Remote work options
    """
    
    response = requests.post(
        f"{BASE_URL}/api/parse-job",
        json={"job_text": job_text}
    )
    
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Title: {data.get('title')}")
        print(f"   Company: {data.get('company')}")
        print(f"   Location: {data.get('location')}")
        print(f"   Sections found: {data.get('sections_found')}")
    else:
        print(f"   Error: {response.text}")
    
    return response.status_code == 200

def main():
    """Run all tests."""
    print("=" * 60)
    print("Resume Coach API - Quick Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 2
    
    if test_health():
        tests_passed += 1
    
    if test_job_parsing():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print("=" * 60)
    
    if tests_passed == total_tests:
        print("✅ All tests passed!")
        print("\nAPI is ready. You can:")
        print("  - View Swagger docs: http://localhost:8000/docs")
        print("  - View ReDoc: http://localhost:8000/redoc")
    else:
        print("❌ Some tests failed. Check the API server logs.")

if __name__ == "__main__":
    main()
