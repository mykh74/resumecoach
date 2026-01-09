#!/usr/bin/env python3
"""
Provider Comparison Tool
Compare OpenAI vs SageMaker performance, quality, and cost.
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.llm_service import LLMService
from backend.models.schema import Resume, JobDescription


def load_test_data() -> tuple[Resume, JobDescription]:
    """Load test resume and job description."""
    # Test resume
    resume = Resume(
        contact_info={
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "555-0123",
            "linkedin": "linkedin.com/in/johndoe"
        },
        summary="Experienced software engineer with 5 years in full-stack development",
        skills=["Python", "JavaScript", "React", "Node.js", "SQL", "Docker"],
        experiences=[
            {
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "duration": "2020-Present",
                "responsibilities": [
                    "Led development of microservices architecture",
                    "Mentored junior developers",
                    "Implemented CI/CD pipelines"
                ]
            }
        ],
        education=[
            {
                "degree": "BS Computer Science",
                "institution": "State University",
                "year": "2018"
            }
        ]
    )
    
    # Test job description
    job = JobDescription(
        title="Staff Software Engineer",
        company="Innovative Startup",
        description="Looking for an experienced engineer to lead backend development",
        required_skills=["Python", "AWS", "Kubernetes", "PostgreSQL", "GraphQL"],
        preferred_skills=["React", "TypeScript", "Terraform"],
        experience_required="5+ years"
    )
    
    return resume, job


def compare_providers(
    test_name: str,
    openai_service: LLMService,
    sagemaker_service: LLMService,
    resume: Resume,
    job: JobDescription
) -> Dict[str, Any]:
    """Compare two providers on the same task."""
    print(f"\n{'='*70}")
    print(f"Test: {test_name}")
    print(f"{'='*70}")
    
    results = {}
    
    # Test OpenAI
    print("\n[1/2] Testing OpenAI...")
    try:
        start_time = time.time()
        openai_report = openai_service.generate_coaching_report(
            resume=resume,
            job_description=job,
            session_id="openai-test"
        )
        openai_time = time.time() - start_time
        
        results["openai"] = {
            "success": True,
            "time": openai_time,
            "fit_score": openai_report.fit_score,
            "summary_length": len(openai_report.summary),
            "num_gaps": len(openai_report.gaps),
            "num_strengths": len(openai_report.strengths),
            "num_recommendations": len(openai_report.recommendations)
        }
        print(f"✓ OpenAI completed in {openai_time:.2f}s")
        print(f"  Fit Score: {openai_report.fit_score}/10")
        print(f"  Gaps: {len(openai_report.gaps)}, Strengths: {len(openai_report.strengths)}")
        
    except Exception as e:
        results["openai"] = {"success": False, "error": str(e)}
        print(f"✗ OpenAI failed: {e}")
    
    # Test SageMaker
    print("\n[2/2] Testing SageMaker...")
    try:
        start_time = time.time()
        sagemaker_report = sagemaker_service.generate_coaching_report(
            resume=resume,
            job_description=job,
            session_id="sagemaker-test"
        )
        sagemaker_time = time.time() - start_time
        
        results["sagemaker"] = {
            "success": True,
            "time": sagemaker_time,
            "fit_score": sagemaker_report.fit_score,
            "summary_length": len(sagemaker_report.summary),
            "num_gaps": len(sagemaker_report.gaps),
            "num_strengths": len(sagemaker_report.strengths),
            "num_recommendations": len(sagemaker_report.recommendations)
        }
        print(f"✓ SageMaker completed in {sagemaker_time:.2f}s")
        print(f"  Fit Score: {sagemaker_report.fit_score}/10")
        print(f"  Gaps: {len(sagemaker_report.gaps)}, Strengths: {len(sagemaker_report.strengths)}")
        
    except Exception as e:
        results["sagemaker"] = {"success": False, "error": str(e)}
        print(f"✗ SageMaker failed: {e}")
    
    # Comparison
    if results["openai"]["success"] and results["sagemaker"]["success"]:
        print(f"\n📊 Comparison:")
        print(f"  Speed: OpenAI={results['openai']['time']:.2f}s vs SageMaker={results['sagemaker']['time']:.2f}s")
        
        speed_winner = "OpenAI" if results["openai"]["time"] < results["sagemaker"]["time"] else "SageMaker"
        speed_diff = abs(results["openai"]["time"] - results["sagemaker"]["time"])
        print(f"  Winner: {speed_winner} (by {speed_diff:.2f}s)")
    
    return results


def estimate_costs(results: Dict[str, Any], monthly_requests: int = 1000):
    """Estimate monthly costs for each provider."""
    print(f"\n{'='*70}")
    print("💰 Cost Estimation")
    print(f"{'='*70}")
    print(f"Assuming {monthly_requests:,} requests per month\n")
    
    # OpenAI costs (rough estimates)
    # GPT-3.5-turbo: $0.002 per 1K tokens
    # Average request: ~1.5K tokens (prompt + response)
    openai_cost_per_request = 0.003  # $0.003 per request
    openai_monthly = openai_cost_per_request * monthly_requests
    
    print(f"OpenAI (gpt-3.5-turbo):")
    print(f"  Cost per request: ~${openai_cost_per_request:.4f}")
    print(f"  Monthly cost: ~${openai_monthly:.2f}")
    
    # SageMaker costs
    # ml.g5.2xlarge: ~$1.41/hour = ~$1,030/month (24/7)
    # But you can stop it when not in use
    sagemaker_hourly = 1.41
    sagemaker_monthly_247 = sagemaker_hourly * 24 * 30
    
    print(f"\nSageMaker (ml.g5.2xlarge):")
    print(f"  Hourly cost: ${sagemaker_hourly:.2f}")
    print(f"  Monthly (24/7): ${sagemaker_monthly_247:.2f}")
    print(f"  Cost per request: ${sagemaker_monthly_247/monthly_requests:.4f} (if running 24/7)")
    
    # Break-even analysis
    breakeven = sagemaker_monthly_247 / openai_cost_per_request
    print(f"\n📈 Break-even Analysis:")
    print(f"  SageMaker becomes cost-effective at ~{breakeven:,.0f} requests/month")
    
    if monthly_requests < breakeven:
        savings = sagemaker_monthly_247 - openai_monthly
        print(f"  💡 Recommendation: Use OpenAI (saves ${savings:.2f}/month)")
    else:
        savings = openai_monthly - sagemaker_monthly_247
        print(f"  💡 Recommendation: Use SageMaker (saves ${savings:.2f}/month)")


def main():
    """Run provider comparison."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare LLM providers")
    parser.add_argument(
        "--monthly-requests",
        type=int,
        default=1000,
        help="Estimated monthly requests for cost analysis"
    )
    parser.add_argument(
        "--skip-sagemaker",
        action="store_true",
        help="Skip SageMaker tests (if endpoint not deployed)"
    )
    
    args = parser.parse_args()
    
    print("="*70)
    print("ResumeCoach Provider Comparison")
    print("="*70)
    
    # Load test data
    print("\nLoading test data...")
    resume, job = load_test_data()
    
    # Initialize services
    print("Initializing LLM services...")
    
    try:
        openai_service = LLMService(provider="openai")
        print("✓ OpenAI service initialized")
    except Exception as e:
        print(f"✗ Failed to initialize OpenAI: {e}")
        return
    
    if not args.skip_sagemaker:
        try:
            sagemaker_service = LLMService(provider="sagemaker")
            print("✓ SageMaker service initialized")
        except Exception as e:
            print(f"✗ Failed to initialize SageMaker: {e}")
            print("\nTo skip SageMaker tests, use --skip-sagemaker")
            return
    else:
        print("⊘ SageMaker tests skipped")
        sagemaker_service = None
    
    # Run comparison tests
    all_results = {}
    
    if sagemaker_service:
        # Test 1: Coaching Report Generation
        results = compare_providers(
            "Coaching Report Generation",
            openai_service,
            sagemaker_service,
            resume,
            job
        )
        all_results["coaching_report"] = results
    
    # Cost estimation
    estimate_costs(all_results, monthly_requests=args.monthly_requests)
    
    # Save results
    output_file = Path(__file__).parent.parent / "comparison_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\n{'='*70}")
    print(f"✅ Comparison complete. Results saved to: {output_file}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
