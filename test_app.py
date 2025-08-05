#!/usr/bin/env python3
"""
Test script for Auto Policy AI Analyzer
Run this to verify your setup before running the main app
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ Google Generative AI")
    except ImportError as e:
        print(f"❌ Google Generative AI import failed: {e}")
        return False
    
    try:
        import pandas
        print(f"✅ Pandas {pandas.__version__}")
    except ImportError as e:
        print(f"❌ Pandas import failed: {e}")
        return False
    
    try:
        import plotly
        print(f"✅ Plotly {plotly.__version__}")
    except ImportError as e:
        print(f"❌ Plotly import failed: {e}")
        return False
    
    try:
        import PIL
        print(f"✅ Pillow {PIL.__version__}")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ Python-dotenv")
    except ImportError as e:
        print(f"❌ Python-dotenv import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        import pdfplumber
        print("✅ pdfplumber")
    except ImportError as e:
        print(f"❌ pdfplumber import failed: {e}")
        return False
    
    return True

def test_config():
    """Test if configuration files can be loaded"""
    print("\nTesting configuration...")
    
    try:
        from config import US_AVERAGES, APP_CONFIG, AI_CONFIG
        print("✅ Configuration loaded successfully")
        print(f"   - US Average Monthly Premium: ${US_AVERAGES['monthly_premium']}")
        print(f"   - App Title: {APP_CONFIG['title']}")
        print(f"   - AI Model: {AI_CONFIG['model']}")
        return True
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False

def test_env_file():
    """Test if environment file exists and has API key"""
    print("\nTesting environment setup...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Load and check API key
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and api_key != 'your_gemini_api_key_here':
            print("✅ Google API key found")
            return True
        else:
            print("⚠️  Google API key not set or using placeholder")
            print("   Please set your GOOGLE_API_KEY in the .env file")
            return False
    else:
        print("❌ .env file not found")
        print("   Please create .env file with your GOOGLE_API_KEY")
        return False

def test_sample_data():
    """Test if sample data file exists"""
    print("\nTesting sample data...")
    
    if os.path.exists('sample_policy.txt'):
        print("✅ Sample policy file found")
        return True
    else:
        print("⚠️  Sample policy file not found")
        return False

def main():
    """Run all tests"""
    print("🚗 Auto Policy AI Analyzer - Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test configuration
    if not test_config():
        all_passed = False
    
    # Test environment
    if not test_env_file():
        all_passed = False
    
    # Test sample data
    if not test_sample_data():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! You're ready to run the app.")
        print("\nTo start the application, run:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above before running the app.")
        print("\nCommon fixes:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Create .env file: cp env_example.txt .env")
        print("3. Add your Google API key to .env file")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 