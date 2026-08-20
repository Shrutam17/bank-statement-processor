#!/usr/bin/env python3
"""Quick test to check Google Gemini availability and list models"""

import os
import sys

def test_gemini():
    """Test Gemini API connection and list available models"""
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not set in environment")
        print("\nGet your FREE API key from: https://aistudio.google.com/app/apikey")
        print("Then run: export GOOGLE_API_KEY='your-key-here'")
        return False
    
    print(f"✅ API key found (length: {len(api_key)})")
    
    # Try to import and initialize
    try:
        import google.generativeai as genai
        print("✅ google-generativeai library installed")
    except ImportError:
        print("❌ google-generativeai not installed")
        print("Install with: pip install google-generativeai")
        return False
    
    # Configure and list models
    try:
        genai.configure(api_key=api_key)
        print("✅ API configured successfully")
        
        print("\n📋 Available Generative Models:")
        print("-" * 60)
        
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  • {model.name}")
                print(f"    Display Name: {model.display_name}")
                print(f"    Description: {model.description[:80]}...")
                print()
        
        # Test a simple generation
        print("\n🧪 Testing model with simple prompt...")
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content("Say 'Hello, Gemini works!'")
        print(f"✅ Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini()
    sys.exit(0 if success else 1)
