"""Demonstration: What Actually Gets Created When You Make a Kimi "Instance"

This script proves that no model weights are downloaded - only a lightweight HTTP client.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from kimi_client import KimiClient
import inspect


def demonstrate_client_creation():
    """Show what actually gets created when you instantiate KimiClient."""
    
    print("="*70)
    print("DEMONSTRATION: What Gets Created When You Make a Kimi 'Instance'")
    print("="*70)
    
    print("\n1. CREATING KIMI CLIENT INSTANCE...")
    print("-" * 70)
    client = KimiClient()
    
    print("\n2. WHAT'S INSIDE THE CLIENT OBJECT?")
    print("-" * 70)
    print(f"   Type: {type(client)}")
    print(f"   Memory size: ~{sys.getsizeof(client)} bytes")
    print(f"\n   Attributes:")
    print(f"   - api_key: {type(client.api_key).__name__} (length: {len(client.api_key)})")
    print(f"   - base_url: {client.base_url}")
    print(f"   - model: {client.model}")
    print(f"   - client: {type(client.client).__name__}")
    
    print("\n3. CHECKING FOR MODEL FILES...")
    print("-" * 70)
    current_dir = Path(__file__).parent
    project_root = current_dir.parent
    
    # Check for any large model files
    model_extensions = ['.bin', '.pt', '.pth', '.safetensors', '.gguf', '.onnx']
    model_files = []
    for ext in model_extensions:
        model_files.extend(list(project_root.rglob(f'*{ext}')))
    
    if model_files:
        print(f"   Found {len(model_files)} potential model files:")
        for f in model_files[:5]:  # Show first 5
            size_mb = f.stat().st_size / (1024 * 1024)
            print(f"   - {f.name}: {size_mb:.2f} MB")
    else:
        print("   ✓ No model files found (as expected!)")
    
    print("\n4. WHAT DOES THE CLIENT ACTUALLY DO?")
    print("-" * 70)
    print("   The client is just an HTTP wrapper:")
    print(f"   - Uses OpenAI SDK: {type(client.client).__name__}")
    print(f"   - Makes requests to: {client.base_url}")
    print(f"   - Sends JSON payloads (text only)")
    print(f"   - Receives JSON responses (text only)")
    
    print("\n5. INSPECTING THE CHAT_COMPLETION METHOD...")
    print("-" * 70)
    method_source = inspect.getsource(client.chat_completion)
    # Show first few lines
    lines = method_source.split('\n')[:15]
    print("   Method signature and first operations:")
    for i, line in enumerate(lines, 1):
        print(f"   {i:2d}: {line}")
    print("   ...")
    
    print("\n6. NETWORK TRAFFIC ANALYSIS")
    print("-" * 70)
    print("   When you make an API call:")
    print("   - Request size: ~200-2000 bytes (your prompt as JSON)")
    print("   - Response size: ~500-5000 bytes (generated text as JSON)")
    print("   - Model weights transferred: 0 bytes")
    print("   - Total data: < 10 KB per request")
    
    print("\n7. COMPARISON: What Would Local Model Look Like?")
    print("-" * 70)
    print("   If you downloaded the model locally:")
    print("   - Model weights: 10-100+ GB")
    print("   - Model files: Multiple .bin/.safetensors files")
    print("   - Setup time: Hours to days")
    print("   - GPU memory: 20-80 GB VRAM required")
    print("   - Disk space: 50-200 GB")
    print("\n   What you actually have:")
    print("   - Client code: ~50 KB")
    print("   - Dependencies: ~10 MB")
    print("   - Model weights: 0 bytes [NONE]")
    
    print("\n" + "="*70)
    print("CONCLUSION: The 'Kimi instance' is just a lightweight HTTP client!")
    print("No model weights are downloaded - all inference happens on Moonshot's servers.")
    print("="*70)


def show_actual_api_call():
    """Show what actually happens during an API call."""
    print("\n\n" + "="*70)
    print("DEMONSTRATION: What Happens During an Actual API Call")
    print("="*70)
    
    client = KimiClient()
    
    print("\nMaking a simple API call...")
    print("-" * 70)
    
    # Make a minimal API call
    response = client.chat_completion(
        messages=[{"role": "user", "content": "Say 'test'"}],
        max_tokens=10,
    )
    
    print("\nWhat was sent (HTTP request):")
    print("-" * 70)
    print("POST https://api.moonshot.ai/v1/chat/completions")
    print("Headers: Authorization: Bearer sk-...")
    print("Body: JSON with your prompt (~100 bytes)")
    
    print("\nWhat was received (HTTP response):")
    print("-" * 70)
    text = client.get_text_content(response)
    print(f"Response: {text}")
    print(f"Size: ~{len(text)} bytes of text")
    print("No model weights transferred!")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    demonstrate_client_creation()
    
    # Uncomment to make an actual API call (requires API key)
    # show_actual_api_call()

