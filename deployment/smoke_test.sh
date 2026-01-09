#!/bin/bash
# Smoke Test Script for Production Deployment
# Tests critical endpoints to verify deployment success

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
API_URL="${1:-http://localhost:8000}"
TIMEOUT=10

echo "🧪 Running Smoke Tests for ResumeCoach"
echo "API URL: $API_URL"
echo "========================================"
echo ""

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to test an endpoint
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local expected_status="$4"
    local data="$5"
    
    echo -n "Testing $name... "
    
    if [ "$method" == "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -m $TIMEOUT "$API_URL$endpoint" 2>/dev/null || echo "000")
    elif [ "$method" == "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST -m $TIMEOUT \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$API_URL$endpoint" 2>/dev/null || echo "000")
    fi
    
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)
    
    if [ "$status_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ PASSED${NC} (Status: $status_code)"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (Expected: $expected_status, Got: $status_code)"
        if [ -n "$body" ]; then
            echo "  Response: $body" | head -c 200
            echo ""
        fi
        ((TESTS_FAILED++))
        return 1
    fi
}

# Test 1: Health Check
test_endpoint "Health Check" "GET" "/api/health" "200"

# Test 2: Root Redirect
test_endpoint "Root Endpoint" "GET" "/" "307"

# Test 3: API Docs
test_endpoint "API Documentation" "GET" "/docs" "200"

# Test 4: Parse Job (with valid data)
JOB_DATA='{"job_description":"Software Engineer with Python experience"}'
test_endpoint "Parse Job Description" "POST" "/api/parse-job" "200" "$JOB_DATA"

# Test 5: Parse Job (empty data - should fail gracefully)
test_endpoint "Parse Job (Invalid)" "POST" "/api/parse-job" "422" '{"job_description":""}'

# Test 6: Upload Resume (without file - should fail)
test_endpoint "Upload Resume (No File)" "POST" "/api/upload-resume" "422"

# Test 7: Session endpoint (should work even without session)
test_endpoint "Get Session" "GET" "/api/session/test-session-123" "200"

# Test 8: LLM Status
test_endpoint "LLM Service Status" "GET" "/api/llm-status" "200"

# Test 9: Switch Provider (should work)
PROVIDER_DATA='{"provider":"openai"}'
test_endpoint "Switch LLM Provider" "POST" "/api/switch-provider" "200" "$PROVIDER_DATA"

# Test 10: Metrics endpoint (if exists)
test_endpoint "Metrics Endpoint" "GET" "/metrics" "404"  # Expected to not exist

echo ""
echo "========================================"
echo "Test Summary:"
echo -e "  ${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "  ${RED}Failed: $TESTS_FAILED${NC}"
echo "========================================"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All smoke tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Check logs for details.${NC}"
    exit 1
fi
