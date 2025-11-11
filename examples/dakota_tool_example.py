"""
Example: Dakota Dictionary Tool for Kimi K2

This script demonstrates how to:
1. Define a Dakota dictionary tool
2. Use it at inference time
3. Handle tool calls and responses
"""

import json
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path

# Import Kimi client (adjust import path as needed)
try:
    from kimik2manim.kimi_client import KimiClient, get_kimi_client
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from kimik2manim.kimi_client import KimiClient, get_kimi_client


# Example Dakota dictionary (replace with your actual dictionary)
EXAMPLE_DAKOTA_DICT = {
    "english_to_dakota": {
        "hello": "hau",
        "thank you": "pilamaya",
        "water": "mni",
        "fire": "peta",
        "earth": "maka",
        "sky": "mahpiya",
        "sun": "wi",
        "moon": "hanwi",
        "star": "wicahpi",
        "tree": "can",
        "bird": "zitkala",
        "dog": "sunka",
        "horse": "sunkawakan",
        "buffalo": "tatanka",
        "eagle": "wanbli"
    },
    "dakota_to_english": {
        "hau": "hello",
        "pilamaya": "thank you",
        "mni": "water",
        "peta": "fire",
        "maka": "earth",
        "mahpiya": "sky",
        "wi": "sun",
        "hanwi": "moon",
        "wicahpi": "star",
        "can": "tree",
        "zitkala": "bird",
        "sunka": "dog",
        "sunkawakan": "horse",
        "tatanka": "buffalo",
        "wanbli": "eagle"
    },
    "definitions": {
        "hau": "A greeting, similar to 'hello' in English",
        "pilamaya": "An expression of gratitude, meaning 'thank you'",
        "mni": "Water, essential for life",
        "tatanka": "Buffalo, sacred animal in Dakota culture"
    }
}


# Tool definition following OpenAI/Kimi format
DAKOTA_DICTIONARY_TOOL = {
    "type": "function",
    "function": {
        "name": "dakota_lookup",
        "description": (
            "Look up words in a comprehensive Dakota language dictionary. "
            "Can translate between English and Dakota, provide definitions, "
            "pronunciations, and cultural context. Use this tool whenever "
            "the user asks about Dakota language, translations, meanings, "
            "or wants to learn Dakota words and phrases."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "word": {
                    "type": "string",
                    "description": "The word or phrase to look up (can be English or Dakota)"
                },
                "query_type": {
                    "type": "string",
                    "enum": [
                        "english_to_dakota",
                        "dakota_to_english",
                        "definition",
                        "all"
                    ],
                    "description": (
                        "Type of lookup: translate English to Dakota, "
                        "Dakota to English, get definition, or get all available information"
                    )
                },
                "context": {
                    "type": "string",
                    "description": "Optional context about how the word will be used (helps with disambiguation)"
                }
            },
            "required": ["word", "query_type"]
        }
    }
}


def dakota_lookup(word: str, query_type: str, context: Optional[str] = None) -> Dict[str, Any]:
    """
    Actual implementation that uses the Dakota dictionary.
    This function gets called when Kimi invokes the tool.
    
    Args:
        word: Word to look up
        query_type: Type of lookup to perform
        context: Optional context
        
    Returns:
        Dictionary with lookup results
    """
    word_lower = word.lower().strip()
    result = {
        "word": word,
        "query_type": query_type,
        "found": False
    }
    
    if query_type == "english_to_dakota":
        translation = EXAMPLE_DAKOTA_DICT.get("english_to_dakota", {}).get(word_lower)
        if translation:
            result.update({
                "found": True,
                "english": word,
                "dakota": translation,
                "definition": EXAMPLE_DAKOTA_DICT.get("definitions", {}).get(translation)
            })
    
    elif query_type == "dakota_to_english":
        translation = EXAMPLE_DAKOTA_DICT.get("dakota_to_english", {}).get(word_lower)
        if translation:
            result.update({
                "found": True,
                "dakota": word,
                "english": translation,
                "definition": EXAMPLE_DAKOTA_DICT.get("definitions", {}).get(word_lower)
            })
    
    elif query_type == "definition":
        definition = EXAMPLE_DAKOTA_DICT.get("definitions", {}).get(word_lower)
        if definition:
            result.update({
                "found": True,
                "word": word,
                "definition": definition
            })
    
    elif query_type == "all":
        # Try all lookups
        eng_to_dak = EXAMPLE_DAKOTA_DICT.get("english_to_dakota", {}).get(word_lower)
        dak_to_eng = EXAMPLE_DAKOTA_DICT.get("dakota_to_english", {}).get(word_lower)
        definition = EXAMPLE_DAKOTA_DICT.get("definitions", {}).get(word_lower)
        
        if eng_to_dak or dak_to_eng or definition:
            result.update({
                "found": True,
                "english_to_dakota": eng_to_dak,
                "dakota_to_english": dak_to_eng,
                "definition": definition
            })
    
    if not result.get("found"):
        result["error"] = f"Word '{word}' not found in dictionary"
        # Suggest similar words
        all_words = list(EXAMPLE_DAKOTA_DICT.get("english_to_dakota", {}).keys())
        suggestions = [w for w in all_words if word_lower in w or w in word_lower][:3]
        if suggestions:
            result["suggestions"] = suggestions
    
    return result


async def ask_with_dakota_tool(question: str) -> str:
    """
    Ask Kimi a question that may require Dakota dictionary lookup.
    
    Args:
        question: User's question
        
    Returns:
        Kimi's final response
    """
    client = get_kimi_client()
    
    # Initial API call with tool definition
    response = client.chat_completion(
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        tools=[DAKOTA_DICTIONARY_TOOL],
        tool_choice="auto",  # Let Kimi decide when to use the tool
        max_tokens=1000
    )
    
    # Check if Kimi called the tool
    if client.has_tool_calls(response):
        tool_calls = client.get_tool_calls(response)
        message = response["choices"][0]["message"]
        
        # Execute tool functions
        tool_responses = []
        for call in tool_calls:
            func_name = call["function"]["name"]
            args_str = call["function"]["arguments"]
            
            try:
                args = json.loads(args_str) if isinstance(args_str, str) else args_str
            except json.JSONDecodeError:
                args = {}
            
            if func_name == "dakota_lookup":
                # Execute the actual lookup function
                tool_result = dakota_lookup(**args)
                tool_responses.append({
                    "role": "tool",
                    "content": json.dumps(tool_result, ensure_ascii=False),
                    "tool_call_id": call.get("id", f"call_{len(tool_responses)}")
                })
        
        # Send tool results back to Kimi for final response
        messages = [
            {"role": "user", "content": question},
            message,  # Assistant's tool call message
            *tool_responses  # Tool execution results
        ]
        
        final_response = client.chat_completion(
            messages=messages,
            tools=[DAKOTA_DICTIONARY_TOOL],
            max_tokens=1000
        )
        
        return client.get_text_content(final_response)
    else:
        # No tool call, return direct response
        return client.get_text_content(response)


async def main():
    """Example usage of Dakota dictionary tool."""
    
    print("=" * 60)
    print("Dakota Dictionary Tool Example")
    print("=" * 60)
    print()
    
    # Example questions
    questions = [
        "What is the Dakota word for 'water'?",
        "How do you say 'thank you' in Dakota?",
        "What does 'tatanka' mean?",
        "Translate 'hello' to Dakota",
        "What is 'mni' in English?",
        "Tell me about the Dakota word for buffalo"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n[{i}] Question: {question}")
        print("-" * 60)
        
        try:
            answer = await ask_with_dakota_tool(question)
            print(f"Answer: {answer}")
        except Exception as e:
            print(f"Error: {e}")
        
        print()


def create_fine_tuning_example() -> Dict[str, Any]:
    """
    Create an example fine-tuning data point.
    This shows the format for training data that includes tool usage.
    """
    return {
        "messages": [
            {
                "role": "user",
                "content": "What is the Dakota word for 'water'?"
            },
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [
                    {
                        "id": "call_001",
                        "type": "function",
                        "function": {
                            "name": "dakota_lookup",
                            "arguments": json.dumps({
                                "word": "water",
                                "query_type": "english_to_dakota"
                            })
                        }
                    }
                ]
            },
            {
                "role": "tool",
                "content": json.dumps({
                    "word": "water",
                    "query_type": "english_to_dakota",
                    "found": True,
                    "english": "water",
                    "dakota": "mni",
                    "definition": "Water, essential for life"
                }),
                "tool_call_id": "call_001"
            },
            {
                "role": "assistant",
                "content": (
                    "The Dakota word for 'water' is **mni**. "
                    "Water is essential for life and holds cultural significance "
                    "in Dakota traditions."
                )
            }
        ],
        "tools": [DAKOTA_DICTIONARY_TOOL]
    }


if __name__ == "__main__":
    # Run example
    asyncio.run(main())
    
    # Show fine-tuning example format
    print("\n" + "=" * 60)
    print("Fine-Tuning Example Format")
    print("=" * 60)
    print(json.dumps(create_fine_tuning_example(), indent=2, ensure_ascii=False))

