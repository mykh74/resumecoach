#!/usr/bin/env python3
"""
Verification script to check if all essential dependencies are installed correctly.
Run this after setting up the virtual environment.
"""

import sys

def check_imports():
    """Check if all essential packages can be imported."""
    required_packages = {
        'langchain': 'LangChain',
        'langchain_community': 'LangChain Community',
        'langchain_openai': 'LangChain OpenAI',
        'openai': 'OpenAI',
        'PyPDF2': 'PyPDF2',
        'pdfplumber': 'PDF Plumber',
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
        'streamlit': 'Streamlit',
        'dotenv': 'Python dotenv',
        'requests': 'Requests',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'pytest': 'Pytest',
    }
    
    print("=" * 60)
    print("Resume Coach - Dependency Verification")
    print("=" * 60)
    print()
    
    failed = []
    for module_name, display_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"✅ {display_name:<25} imported successfully")
        except ImportError as e:
            print(f"❌ {display_name:<25} FAILED: {e}")
            failed.append(display_name)
    
    print()
    print("=" * 60)
    
    if failed:
        print(f"❌ {len(failed)} package(s) failed to import:")
        for pkg in failed:
            print(f"   - {pkg}")
        print()
        print("Please install missing packages:")
        print("  pip install -r requirements-core.txt")
        sys.exit(1)
    else:
        print("✅ All essential packages imported successfully!")
        print()
        print("Python version:", sys.version)
        print()
        print("You're ready to start development! 🚀")
        print()
        print("Next steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your OpenAI API key to .env")
        print("  3. Start with Day 1 tasks (see PROJECT_PLAN.md)")
    
    return len(failed) == 0

if __name__ == "__main__":
    success = check_imports()
    sys.exit(0 if success else 1)
