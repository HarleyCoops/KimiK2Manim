"""
Utility: Convert Dakota Dictionary to Kimi Tool Format

This script helps convert your Dakota dictionary file into:
1. Tool definition JSON schema
2. Fine-tuning examples (optional)
3. Python code for tool implementation
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List


def analyze_dictionary_structure(dakota_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the structure of a Dakota dictionary to understand its format.
    
    Returns:
        Dictionary with structure analysis
    """
    analysis = {
        "has_english_to_dakota": False,
        "has_dakota_to_english": False,
        "has_definitions": False,
        "has_pronunciations": False,
        "has_examples": False,
        "has_metadata": False,
        "sample_keys": [],
        "structure_type": "unknown"
    }
    
    # Check for common structures
    if "english_to_dakota" in dakota_dict:
        analysis["has_english_to_dakota"] = True
        analysis["sample_keys"].extend(list(dakota_dict["english_to_dakota"].keys())[:5])
    
    if "dakota_to_english" in dakota_dict:
        analysis["has_dakota_to_english"] = True
    
    if "definitions" in dakota_dict:
        analysis["has_definitions"] = True
    
    # Check if it's a simple flat dictionary
    if not any(key in dakota_dict for key in ["english_to_dakota", "dakota_to_english", "definitions"]):
        # Might be a simple key-value mapping
        sample_key = list(dakota_dict.keys())[0] if dakota_dict else None
        if sample_key:
            sample_value = dakota_dict[sample_key]
            if isinstance(sample_value, str):
                analysis["structure_type"] = "simple_key_value"
            elif isinstance(sample_value, dict):
                analysis["structure_type"] = "rich_entries"
                if "pronunciation" in sample_value:
                    analysis["has_pronunciations"] = True
                if "examples" in sample_value:
                    analysis["has_examples"] = True
                if "definition" in sample_value or "meaning" in sample_value:
                    analysis["has_definitions"] = True
    
    return analysis


def create_tool_definition(analysis: Dict[str, Any], custom_description: str = None) -> Dict[str, Any]:
    """
    Create a tool definition based on dictionary structure analysis.
    
    Args:
        analysis: Structure analysis from analyze_dictionary_structure
        custom_description: Optional custom description for the tool
        
    Returns:
        Tool definition in OpenAI/Kimi format
    """
    # Determine query types based on available data
    query_types = []
    if analysis["has_english_to_dakota"]:
        query_types.append("english_to_dakota")
    if analysis["has_dakota_to_english"]:
        query_types.append("dakota_to_english")
    if analysis["has_definitions"]:
        query_types.append("definition")
    if analysis["has_examples"]:
        query_types.append("examples")
    if analysis["has_pronunciations"]:
        query_types.append("pronunciation")
    
    if not query_types:
        query_types = ["translate", "define", "all"]
    
    # Build description
    if custom_description:
        description = custom_description
    else:
        description = (
            "Look up words in a comprehensive Dakota language dictionary. "
            "Can translate between English and Dakota"
        )
        if analysis["has_definitions"]:
            description += ", provide definitions"
        if analysis["has_examples"]:
            description += ", usage examples"
        if analysis["has_pronunciations"]:
            description += ", pronunciations"
        description += ". Use this tool whenever the user asks about Dakota language."
    
    # Build parameters
    properties = {
        "word": {
            "type": "string",
            "description": "The word or phrase to look up (can be English or Dakota)"
        },
        "query_type": {
            "type": "string",
            "enum": query_types + ["all"],
            "description": f"Type of lookup: {', '.join(query_types)}, or 'all' for complete information"
        }
    }
    
    # Add optional context parameter
    properties["context"] = {
        "type": "string",
        "description": "Optional context about how the word will be used (helps with disambiguation)"
    }
    
    # Add dialect if metadata suggests multiple dialects
    if analysis["has_metadata"]:
        properties["dialect"] = {
            "type": "string",
            "enum": ["santee", "yankton", "yanktonai", "lakota", "auto"],
            "description": "Dakota dialect variant",
            "default": "auto"
        }
    
    tool_def = {
        "type": "function",
        "function": {
            "name": "dakota_lookup",
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": ["word", "query_type"]
            }
        }
    }
    
    return tool_def


def create_implementation_template(analysis: Dict[str, Any], dict_var_name: str = "DAKOTA_DICT") -> str:
    """
    Generate Python code template for implementing the lookup function.
    
    Args:
        analysis: Structure analysis
        dict_var_name: Name of the dictionary variable
        
    Returns:
        Python code string
    """
    code = f'''def dakota_lookup(word: str, query_type: str, context: str = None) -> Dict[str, Any]:
    """
    Look up words in Dakota dictionary.
    
    Args:
        word: Word to look up
        query_type: Type of lookup
        context: Optional context
        
    Returns:
        Dictionary with lookup results
    """
    word_lower = word.lower().strip()
    result = {{
        "word": word,
        "query_type": query_type,
        "found": False
    }}
    
    # Load your dictionary (replace with actual loading logic)
    dakota_dict = {dict_var_name}
    
'''
    
    if analysis["has_english_to_dakota"]:
        code += '''    if query_type == "english_to_dakota":
        translation = dakota_dict.get("english_to_dakota", {}).get(word_lower)
        if translation:
            result.update({
                "found": True,
                "english": word,
                "dakota": translation
            })
    
'''
    
    if analysis["has_dakota_to_english"]:
        code += '''    elif query_type == "dakota_to_english":
        translation = dakota_dict.get("dakota_to_english", {}).get(word_lower)
        if translation:
            result.update({
                "found": True,
                "dakota": word,
                "english": translation
            })
    
'''
    
    if analysis["has_definitions"]:
        code += '''    elif query_type == "definition":
        definition = dakota_dict.get("definitions", {}).get(word_lower)
        if definition:
            result.update({
                "found": True,
                "word": word,
                "definition": definition
            })
    
'''
    
    code += '''    elif query_type == "all":
        # Try all available lookups
        # ... implement comprehensive lookup
    
    if not result.get("found"):
        result["error"] = f"Word '{word}' not found"
    
    return result
'''
    
    return code


def create_fine_tuning_examples(
    dakota_dict: Dict[str, Any],
    analysis: Dict[str, Any],
    num_examples: int = 10
) -> List[Dict[str, Any]]:
    """
    Generate fine-tuning examples from dictionary entries.
    
    Args:
        dakota_dict: The Dakota dictionary
        analysis: Structure analysis
        num_examples: Number of examples to generate
        
    Returns:
        List of fine-tuning examples
    """
    examples = []
    
    # Get sample entries
    if analysis["has_english_to_dakota"]:
        eng_to_dak = dakota_dict.get("english_to_dakota", {})
        sample_words = list(eng_to_dak.keys())[:num_examples]
        
        for i, word in enumerate(sample_words):
            dakota_word = eng_to_dak[word]
            example = {
                "messages": [
                    {
                        "role": "user",
                        "content": f"What is the Dakota word for '{word}'?"
                    },
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": f"call_{i:03d}",
                            "type": "function",
                            "function": {
                                "name": "dakota_lookup",
                                "arguments": json.dumps({
                                    "word": word,
                                    "query_type": "english_to_dakota"
                                })
                            }
                        }]
                    },
                    {
                        "role": "tool",
                        "content": json.dumps({
                            "word": word,
                            "query_type": "english_to_dakota",
                            "found": True,
                            "english": word,
                            "dakota": dakota_word
                        }),
                        "tool_call_id": f"call_{i:03d}"
                    },
                    {
                        "role": "assistant",
                        "content": f"The Dakota word for '{word}' is **{dakota_word}**."
                    }
                ]
            }
            examples.append(example)
    
    return examples


def main():
    parser = argparse.ArgumentParser(
        description="Convert Dakota dictionary to Kimi tool format"
    )
    parser.add_argument(
        "dictionary_file",
        type=str,
        help="Path to Dakota dictionary JSON file"
    )
    parser.add_argument(
        "--output-tool",
        type=str,
        help="Output file for tool definition JSON (default: dakota_tool.json)"
    )
    parser.add_argument(
        "--output-code",
        type=str,
        help="Output file for Python implementation template (default: dakota_lookup.py)"
    )
    parser.add_argument(
        "--output-finetuning",
        type=str,
        help="Output file for fine-tuning examples JSONL (optional)"
    )
    parser.add_argument(
        "--num-examples",
        type=int,
        default=10,
        help="Number of fine-tuning examples to generate (default: 10)"
    )
    parser.add_argument(
        "--description",
        type=str,
        help="Custom description for the tool"
    )
    
    args = parser.parse_args()
    
    # Load dictionary
    dict_path = Path(args.dictionary_file)
    if not dict_path.exists():
        print(f"Error: Dictionary file not found: {dict_path}")
        return
    
    with open(dict_path, 'r', encoding='utf-8') as f:
        dakota_dict = json.load(f)
    
    print(f"Loaded dictionary from: {dict_path}")
    print(f"Dictionary has {len(dakota_dict)} top-level keys")
    
    # Analyze structure
    print("\nAnalyzing dictionary structure...")
    analysis = analyze_dictionary_structure(dakota_dict)
    print(f"Structure type: {analysis['structure_type']}")
    print(f"Has English->Dakota: {analysis['has_english_to_dakota']}")
    print(f"Has Dakota->English: {analysis['has_dakota_to_english']}")
    print(f"Has definitions: {analysis['has_definitions']}")
    print(f"Has pronunciations: {analysis['has_pronunciations']}")
    print(f"Has examples: {analysis['has_examples']}")
    
    # Create tool definition
    print("\nCreating tool definition...")
    tool_def = create_tool_definition(analysis, args.description)
    
    # Save tool definition
    output_tool = args.output_tool or "dakota_tool.json"
    with open(output_tool, 'w', encoding='utf-8') as f:
        json.dump(tool_def, f, indent=2, ensure_ascii=False)
    print(f"Saved tool definition to: {output_tool}")
    
    # Create implementation template
    if args.output_code:
        print("\nCreating implementation template...")
        impl_code = create_implementation_template(analysis)
        with open(args.output_code, 'w', encoding='utf-8') as f:
            f.write(impl_code)
        print(f"Saved implementation template to: {args.output_code}")
    
    # Create fine-tuning examples
    if args.output_finetuning:
        print(f"\nCreating {args.num_examples} fine-tuning examples...")
        examples = create_fine_tuning_examples(dakota_dict, analysis, args.num_examples)
        
        with open(args.output_finetuning, 'w', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + "\n")
        print(f"Saved fine-tuning examples to: {args.output_finetuning}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()

