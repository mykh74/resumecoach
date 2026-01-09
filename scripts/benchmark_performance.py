#!/usr/bin/env python3
"""
Performance Benchmarking Suite for Resume Coach

Measures and tracks performance of all major operations to detect regressions
and identify optimization opportunities.

Usage:
    python scripts/benchmark_performance.py
    python scripts/benchmark_performance.py --output results/benchmarks.json
    python scripts/benchmark_performance.py --compare results/baseline.json
"""
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import statistics

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.services.resume_parser import ResumeParser
from backend.services.job_parser import JobParser
from backend.services.llm_service import LLMService
from backend.models.schema import Resume, JobDescription

# Benchmark configuration
NUM_ITERATIONS = 5  # Number of times to run each benchmark
SAMPLE_RESUME_PATH = "data/sample_resumes/john_doe_resume.pdf"
SAMPLE_JOB_PATH = "data/job_postings/senior_fullstack_ml_job.md"


class BenchmarkResults:
    """Store and analyze benchmark results."""
    
    def __init__(self):
        self.results = {}
        self.metadata = {
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version,
            "iterations": NUM_ITERATIONS
        }
    
    def add_result(self, name: str, times: List[float], metadata: Dict = None):
        """Add benchmark result."""
        self.results[name] = {
            "times": times,
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "min": min(times),
            "max": max(times),
            "p95": sorted(times)[int(len(times) * 0.95)] if len(times) > 1 else times[0],
            "metadata": metadata or {}
        }
    
    def print_summary(self):
        """Print benchmark summary."""
        print("\n" + "="*80)
        print("📊 Performance Benchmark Results")
        print("="*80)
        print(f"Timestamp: {self.metadata['timestamp']}")
        print(f"Iterations: {self.metadata['iterations']}")
        print("="*80 + "\n")
        
        for name, data in self.results.items():
            print(f"🔹 {name}")
            print(f"   Mean:   {data['mean']*1000:.2f}ms")
            print(f"   Median: {data['median']*1000:.2f}ms")
            print(f"   P95:    {data['p95']*1000:.2f}ms")
            print(f"   Min:    {data['min']*1000:.2f}ms")
            print(f"   Max:    {data['max']*1000:.2f}ms")
            if data['stdev'] > 0:
                print(f"   StdDev: {data['stdev']*1000:.2f}ms")
            if data['metadata']:
                for key, value in data['metadata'].items():
                    print(f"   {key}: {value}")
            print()
    
    def save(self, filepath: str):
        """Save results to JSON file."""
        output = {
            "metadata": self.metadata,
            "results": self.results
        }
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"✅ Results saved to: {filepath}")
    
    def compare(self, baseline_path: str):
        """Compare with baseline results."""
        if not Path(baseline_path).exists():
            print(f"⚠️ Baseline file not found: {baseline_path}")
            return
        
        with open(baseline_path) as f:
            baseline = json.load(f)
        
        print("\n" + "="*80)
        print("📈 Performance Comparison (vs Baseline)")
        print("="*80)
        
        for name, current in self.results.items():
            if name in baseline['results']:
                baseline_mean = baseline['results'][name]['mean']
                current_mean = current['mean']
                diff = ((current_mean - baseline_mean) / baseline_mean) * 100
                
                status = "🟢" if diff <= 5 else "🟡" if diff <= 15 else "🔴"
                print(f"{status} {name}")
                print(f"   Current:  {current_mean*1000:.2f}ms")
                print(f"   Baseline: {baseline_mean*1000:.2f}ms")
                print(f"   Change:   {diff:+.1f}%")
            else:
                print(f"🆕 {name} (new benchmark)")
                print(f"   Current: {current['mean']*1000:.2f}ms")
            print()


def benchmark_function(func, *args, **kwargs) -> float:
    """Benchmark a single function call."""
    start = time.time()
    func(*args, **kwargs)
    return time.time() - start


def benchmark_resume_parsing(results: BenchmarkResults):
    """Benchmark resume parsing operations."""
    print("🔄 Benchmarking resume parsing...")
    
    parser = ResumeParser()
    resume_path = Path(SAMPLE_RESUME_PATH)
    
    if not resume_path.exists():
        print(f"⚠️ Sample resume not found: {SAMPLE_RESUME_PATH}")
        return
    
    # Get file size
    file_size = resume_path.stat().st_size
    
    # Benchmark full parsing
    times = []
    for i in range(NUM_ITERATIONS):
        print(f"  Iteration {i+1}/{NUM_ITERATIONS}...", end='\r')
        t = benchmark_function(parser.parse_resume, str(resume_path))
        times.append(t)
    
    results.add_result(
        "Resume Parsing (Full)",
        times,
        {"file_size": f"{file_size/1024:.1f} KB"}
    )
    print("  ✓ Resume parsing complete" + " "*20)


def benchmark_job_parsing(results: BenchmarkResults):
    """Benchmark job description parsing."""
    print("🔄 Benchmarking job parsing...")
    
    parser = JobParser()
    job_path = Path(SAMPLE_JOB_PATH)
    
    if not job_path.exists():
        print(f"⚠️ Sample job description not found: {SAMPLE_JOB_PATH}")
        # Use default text
        job_text = """
        Senior Full Stack Engineer
        
        We are seeking an experienced engineer with:
        - 5+ years of software development
        - Python, JavaScript, React expertise
        - AWS cloud experience
        - Strong problem-solving skills
        """
    else:
        job_text = job_path.read_text()
    
    # Get text length
    text_length = len(job_text)
    
    # Benchmark full parsing
    times = []
    for i in range(NUM_ITERATIONS):
        print(f"  Iteration {i+1}/{NUM_ITERATIONS}...", end='\r')
        t = benchmark_function(parser.parse_job_description, job_text)
        times.append(t)
    
    results.add_result(
        "Job Parsing (Full)",
        times,
        {"text_length": f"{text_length} chars"}
    )
    print("  ✓ Job parsing complete" + " "*20)


def benchmark_llm_operations(results: BenchmarkResults, skip_llm: bool = False):
    """Benchmark LLM service operations."""
    if skip_llm:
        print("⏭️  Skipping LLM benchmarks (use --with-llm to enable)")
        return
    
    print("🔄 Benchmarking LLM operations (this may take a while)...")
    print("⚠️  Note: Requires valid OpenAI API key in .env")
    
    try:
        llm_service = LLMService(provider="openai")
    except Exception as e:
        print(f"⚠️ Could not initialize LLM service: {e}")
        print("   Skipping LLM benchmarks")
        return
    
    # Create sample data
    sample_resume = Resume(
        full_text="John Doe\nSoftware Engineer\n5 years experience\nPython, JavaScript, React",
        skills=["Python", "JavaScript", "React"],
        experience_years=5,
        education=["Bachelor's in Computer Science"],
        contact_info={"email": "john@example.com"}
    )
    
    sample_job = JobDescription(
        full_text="Senior Engineer position requiring Python and React",
        required_skills=["Python", "React", "AWS"],
        experience_level="Senior",
        job_type="Full-time"
    )
    
    # Benchmark coaching report generation
    print("  Testing coaching report generation...")
    times = []
    for i in range(min(3, NUM_ITERATIONS)):  # Fewer iterations for LLM (expensive)
        print(f"  Iteration {i+1}/{min(3, NUM_ITERATIONS)}...", end='\r')
        try:
            start = time.time()
            llm_service.generate_coaching_report(
                resume=sample_resume,
                job_description=sample_job,
                session_id=f"benchmark-{i}"
            )
            times.append(time.time() - start)
        except Exception as e:
            print(f"\n⚠️ LLM call failed: {e}")
            break
    
    if times:
        results.add_result(
            "LLM Coaching Report Generation",
            times,
            {"provider": "openai", "model": "gpt-3.5-turbo"}
        )
        print("  ✓ LLM benchmarks complete" + " "*20)


def benchmark_all(output_file: str = None, baseline_file: str = None, with_llm: bool = False):
    """Run all benchmarks."""
    results = BenchmarkResults()
    
    print("\n" + "="*80)
    print("🚀 Starting Performance Benchmarks")
    print("="*80)
    print(f"Iterations per test: {NUM_ITERATIONS}")
    print(f"LLM testing: {'Enabled' if with_llm else 'Disabled (use --with-llm to enable)'}")
    print("="*80 + "\n")
    
    # Run benchmarks
    benchmark_resume_parsing(results)
    benchmark_job_parsing(results)
    benchmark_llm_operations(results, skip_llm=not with_llm)
    
    # Print results
    results.print_summary()
    
    # Save if output file specified
    if output_file:
        results.save(output_file)
    
    # Compare with baseline if specified
    if baseline_file:
        results.compare(baseline_file)
    
    print("="*80)
    print("✅ Benchmarking Complete")
    print("="*80 + "\n")


def create_baseline():
    """Create baseline benchmark results."""
    print("📊 Creating baseline benchmark results...")
    output_file = "results/baseline_benchmarks.json"
    benchmark_all(output_file=output_file, with_llm=False)
    print(f"\n✅ Baseline created: {output_file}")
    print("💡 Use this file to compare future performance changes:")
    print(f"   python scripts/benchmark_performance.py --compare {output_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Performance benchmarking suite for Resume Coach",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all benchmarks
  python scripts/benchmark_performance.py
  
  # Save results to file
  python scripts/benchmark_performance.py --output results/benchmarks.json
  
  # Compare with baseline
  python scripts/benchmark_performance.py --compare results/baseline.json
  
  # Include LLM benchmarks (requires API key)
  python scripts/benchmark_performance.py --with-llm
  
  # Create baseline for future comparisons
  python scripts/benchmark_performance.py --create-baseline
        """
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Save results to JSON file',
        metavar='FILE'
    )
    
    parser.add_argument(
        '--compare', '-c',
        help='Compare results with baseline file',
        metavar='FILE'
    )
    
    parser.add_argument(
        '--with-llm',
        action='store_true',
        help='Include LLM benchmarks (slower, requires API key)'
    )
    
    parser.add_argument(
        '--create-baseline',
        action='store_true',
        help='Create baseline benchmark file for future comparisons'
    )
    
    parser.add_argument(
        '--iterations', '-n',
        type=int,
        default=NUM_ITERATIONS,
        help=f'Number of iterations per test (default: {NUM_ITERATIONS})'
    )
    
    args = parser.parse_args()
    
    # Update global iterations if specified
    global NUM_ITERATIONS
    NUM_ITERATIONS = args.iterations
    
    if args.create_baseline:
        create_baseline()
    else:
        benchmark_all(
            output_file=args.output,
            baseline_file=args.compare,
            with_llm=args.with_llm
        )


if __name__ == "__main__":
    main()
