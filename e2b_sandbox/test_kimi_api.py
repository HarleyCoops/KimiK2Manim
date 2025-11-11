"""Test script for Kimi API connection - new instance for testing."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Load environment variables
load_dotenv()

# Import KimiClient
try:
    from kimi_client import KimiClient
except ImportError:
    print("Error: Could not import KimiClient. Make sure you're running from the project root.")
    sys.exit(1)


def test_connection():
    """Test basic API connection to Kimi."""
    print("\n" + "="*70)
    print("Testing Kimi API Connection")
    print("="*70)
    
    # Check API key
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        print("[ERROR] MOONSHOT_API_KEY not set!")
        print("\nPlease set it in your .env file:")
        print("  MOONSHOT_API_KEY=your_key_here")
        return False
    
    # Show masked API key for debugging
    masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
    print(f"[INFO] API Key loaded: {masked_key}")
    print(f"[INFO] API Key length: {len(api_key)}")
    
    # Create new KimiClient instance
    print("\n[INFO] Creating new KimiClient instance...")
    try:
        client = KimiClient()
        print(f"[INFO] Client initialized successfully")
        print(f"[INFO] Model: {client.model}")
        print(f"[INFO] Base URL: {client.base_url}")
    except Exception as e:
        print(f"[ERROR] Failed to initialize client: {e}")
        return False
    
    # Test basic chat completion
    print("\n[INFO] Testing basic chat completion...")
    try:
        response = client.chat_completion(
            messages=[
                {"role": "user", "content": "Say 'Hello, API connection successful!' in one sentence."}
            ],
            max_tokens=50,
        )
        
        text_content = client.get_text_content(response)
        print(f"[SUCCESS] Response received: {text_content}")
        
        # Show usage stats if available
        if 'usage' in response:
            usage = response['usage']
            print(f"[INFO] Token usage: {usage}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_queries():
    """Test multiple queries to verify connection stability."""
    print("\n" + "="*70)
    print("Testing Multiple Queries")
    print("="*70)
    
    client = KimiClient()
    
    test_queries = [
        "What is 2+2? Answer in one word.",
        "What is the capital of France? Answer in one word.",
        "Say 'test successful' if you can read this.",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[TEST {i}/{len(test_queries)}] Query: {query}")
        try:
            response = client.chat_completion(
                messages=[{"role": "user", "content": query}],
                max_tokens=30,
            )
            text_content = client.get_text_content(response)
            print(f"[RESULT] {text_content}")
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            return False
    
    print("\n[SUCCESS] All queries completed successfully!")
    return True


def main():
    """Run all tests."""
    print("""
======================================================================
          Kimi API Connection Test - New Instance
======================================================================
    """)
    
    # Run tests
    success = True
    
    if not test_connection():
        success = False
    
    if success:
        if not test_multiple_queries():
            success = False
    
    print("\n" + "="*70)
    if success:
        print("All tests passed! [SUCCESS]")
    else:
        print("Some tests failed! [FAILED]")
    print("="*70)


if __name__ == "__main__":
    main()

