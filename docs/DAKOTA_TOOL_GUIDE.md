# Dakota Dictionary Tool Guide for Kimi K2

This guide explains how to convert a Dakota dictionary into a custom tool that can be used with Kimi K2 API, both at inference time and potentially during fine-tuning.

## Understanding Kimi Tool Calling

Kimi K2 uses an **OpenAI-compatible function calling format**. Tools are defined as JSON schemas that describe:
- **Function name**: What the tool is called
- **Description**: What the tool does (helps the model decide when to use it)
- **Parameters**: Input schema using JSON Schema format

### Tool Definition Format

```python
DAKOTA_TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_dakota",
        "description": "Look up Dakota language translations, definitions, or usage examples from a comprehensive Dakota dictionary.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The English word, phrase, or Dakota word to look up"
                },
                "query_type": {
                    "type": "string",
                    "enum": ["english_to_dakota", "dakota_to_english", "definition", "example"],
                    "description": "Type of lookup: translate English to Dakota, Dakota to English, get definition, or get usage examples"
                },
                "context": {
                    "type": "string",
                    "description": "Optional context about how the word will be used (helps disambiguate)"
                }
            },
            "required": ["query", "query_type"]
        }
    }
}
```

## Converting Your Dakota Dictionary

### Step 1: Understand Your Dictionary Structure

First, identify the structure of your Dakota dictionary. Common formats include:

**Format A: Simple Key-Value**
```python
dakota_dict = {
    "hello": "hau",
    "thank you": "pilamaya",
    "water": "mni"
}
```

**Format B: Rich Dictionary with Metadata**
```python
dakota_dict = {
    "hello": {
        "dakota": "hau",
        "pronunciation": "how",
        "part_of_speech": "interjection",
        "examples": ["Hau, mitakuyepi", "Hau, tanyan yahi"]
    }
}
```

**Format C: Bidirectional**
```python
dakota_dict = {
    "english_to_dakota": {
        "hello": "hau",
        "water": "mni"
    },
    "dakota_to_english": {
        "hau": "hello",
        "mni": "water"
    }
}
```

### Step 2: Design Your Tool Schema

Based on your dictionary structure, design a tool that:
1. **Matches your data structure** - parameters should align with what your dictionary contains
2. **Is discoverable** - clear description so Kimi knows when to use it
3. **Handles edge cases** - optional parameters for context, variants, etc.

**Example: Simple Translation Tool**
```python
DAKOTA_TRANSLATION_TOOL = {
    "type": "function",
    "function": {
        "name": "translate_dakota",
        "description": "Translate between English and Dakota language using a comprehensive dictionary. Use this when the user asks about Dakota translations, meanings, or wants to learn Dakota words.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to translate (English or Dakota)"
                },
                "direction": {
                    "type": "string",
                    "enum": ["to_dakota", "to_english", "auto"],
                    "description": "Translation direction. Use 'auto' to detect automatically.",
                    "default": "auto"
                }
            },
            "required": ["text"]
        }
    }
}
```

**Example: Rich Dictionary Tool with Multiple Operations**
```python
DAKOTA_DICTIONARY_TOOL = {
    "type": "function",
    "function": {
        "name": "dakota_dictionary_lookup",
        "description": "Comprehensive Dakota language dictionary tool. Can translate, provide definitions, pronunciations, usage examples, and cultural context for Dakota words and phrases.",
        "parameters": {
            "type": "object",
            "properties": {
                "word": {
                    "type": "string",
                    "description": "The word or phrase to look up (English or Dakota)"
                },
                "operation": {
                    "type": "string",
                    "enum": ["translate", "define", "pronounce", "examples", "etymology", "cultural_context"],
                    "description": "What information to retrieve about the word"
                },
                "dialect": {
                    "type": "string",
                    "enum": ["santee", "yankton", "yanktonai", "lakota", "auto"],
                    "description": "Dakota dialect variant (optional, defaults to auto-detect)",
                    "default": "auto"
                }
            },
            "required": ["word", "operation"]
        }
    }
}
```

## Using Tools at Inference Time

### Basic Usage Pattern

```python
from kimik2manim.kimi_client import KimiClient

client = KimiClient()

# Your Dakota dictionary (loaded from file, database, etc.)
DAKOTA_DICT = {
    "hello": "hau",
    "thank you": "pilamaya",
    "water": "mni",
    # ... more entries
}

def lookup_dakota(word: str, operation: str = "translate") -> dict:
    """Actual function that uses your dictionary."""
    if operation == "translate":
        # Simple lookup logic
        result = DAKOTA_DICT.get(word.lower(), "Not found")
        return {"translation": result, "original": word}
    # ... handle other operations
    return {"error": "Operation not supported"}

# Define your tool
DAKOTA_TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_dakota",
        "description": "Look up Dakota translations...",
        "parameters": {
            # ... your schema
        }
    }
}

# Make API call with tool
response = client.chat_completion(
    messages=[
        {"role": "user", "content": "How do you say 'thank you' in Dakota?"}
    ],
    tools=[DAKOTA_TOOL],
    tool_choice="auto"  # Let Kimi decide when to use the tool
)

# Check if Kimi called the tool
if client.has_tool_calls(response):
    tool_calls = client.get_tool_calls(response)
    for call in tool_calls:
        func_name = call["function"]["name"]
        args = json.loads(call["function"]["arguments"])
        
        if func_name == "lookup_dakota":
            # Execute your actual function
            result = lookup_dakota(**args)
            
            # Send result back to Kimi (tool response)
            tool_response = client.chat_completion(
                messages=[
                    {"role": "user", "content": "How do you say 'thank you' in Dakota?"},
                    {"role": "assistant", "content": None, "tool_calls": tool_calls},
                    {
                        "role": "tool",
                        "content": json.dumps(result),
                        "tool_call_id": call["id"]
                    }
                ],
                tools=[DAKOTA_TOOL]
            )
            
            final_answer = client.get_text_content(tool_response)
            print(final_answer)
```

### Complete Example: Dakota Dictionary Tool

```python
import json
from kimik2manim.kimi_client import KimiClient, get_kimi_client

# Load your Dakota dictionary
def load_dakota_dictionary(file_path: str) -> dict:
    """Load Dakota dictionary from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Your actual dictionary lookup function
def dakota_lookup(word: str, query_type: str, context: str = None) -> dict:
    """
    Actual implementation that uses your Dakota dictionary.
    This is what gets executed when Kimi calls the tool.
    """
    dakota_dict = load_dakota_dictionary("dakota_dictionary.json")
    
    word_lower = word.lower()
    
    if query_type == "english_to_dakota":
        result = dakota_dict.get("english_to_dakota", {}).get(word_lower)
        return {
            "english": word,
            "dakota": result,
            "found": result is not None
        }
    elif query_type == "dakota_to_english":
        result = dakota_dict.get("dakota_to_english", {}).get(word_lower)
        return {
            "dakota": word,
            "english": result,
            "found": result is not None
        }
    # ... handle other query types
    
    return {"error": "Invalid query type"}

# Tool definition
DAKOTA_DICTIONARY_TOOL = {
    "type": "function",
    "function": {
        "name": "dakota_lookup",
        "description": (
            "Look up words in a comprehensive Dakota language dictionary. "
            "Can translate between English and Dakota, provide definitions, "
            "pronunciations, and usage examples. Use this whenever the user "
            "asks about Dakota language, translations, or wants to learn Dakota words."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "word": {
                    "type": "string",
                    "description": "The word or phrase to look up"
                },
                "query_type": {
                    "type": "string",
                    "enum": ["english_to_dakota", "dakota_to_english", "definition", "example"],
                    "description": "Type of lookup to perform"
                },
                "context": {
                    "type": "string",
                    "description": "Optional context about usage (helps with disambiguation)"
                }
            },
            "required": ["word", "query_type"]
        }
    }
}

# Usage
async def ask_about_dakota(question: str):
    client = get_kimi_client()
    
    response = client.chat_completion(
        messages=[{"role": "user", "content": question}],
        tools=[DAKOTA_DICTIONARY_TOOL],
        tool_choice="auto"
    )
    
    # Handle tool calls
    if client.has_tool_calls(response):
        tool_calls = client.get_tool_calls(response)
        
        # Execute tool functions
        tool_responses = []
        for call in tool_calls:
            func_name = call["function"]["name"]
            args = json.loads(call["function"]["arguments"])
            
            if func_name == "dakota_lookup":
                result = dakota_lookup(**args)
                tool_responses.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": call["id"]
                })
        
        # Send tool results back to Kimi
        messages = [
            {"role": "user", "content": question},
            response["choices"][0]["message"],
            *tool_responses
        ]
        
        final_response = client.chat_completion(
            messages=messages,
            tools=[DAKOTA_DICTIONARY_TOOL]
        )
        
        return client.get_text_content(final_response)
    else:
        return client.get_text_content(response)

# Example usage
result = await ask_about_dakota("What is the Dakota word for 'water'?")
print(result)
```

## Using Tools During Fine-Tuning

### Understanding Fine-Tuning with Tools

When fine-tuning Kimi K2, you can include tool definitions and tool call examples in your training data. This teaches the model:
1. **When to use tools** - based on user queries
2. **How to format tool calls** - correct parameter structure
3. **How to interpret tool results** - using tool responses in context

### Fine-Tuning Data Format

Your fine-tuning dataset should include examples like:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "How do you say 'hello' in Dakota?"
    },
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "dakota_lookup",
            "arguments": "{\"word\": \"hello\", \"query_type\": \"english_to_dakota\"}"
          }
        }
      ]
    },
    {
      "role": "tool",
      "content": "{\"english\": \"hello\", \"dakota\": \"hau\", \"found\": true}",
      "tool_call_id": "call_abc123"
    },
    {
      "role": "assistant",
      "content": "The Dakota word for 'hello' is **hau** (pronounced 'how'). It's a common greeting in Dakota culture."
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "dakota_lookup",
        "description": "Look up words in Dakota dictionary...",
        "parameters": {
          "type": "object",
          "properties": {
            "word": {"type": "string"},
            "query_type": {"type": "string", "enum": ["english_to_dakota", "dakota_to_english"]}
          },
          "required": ["word", "query_type"]
        }
      }
    }
  ]
}
```

### Creating Fine-Tuning Dataset

```python
def create_fine_tuning_examples(dakota_dict: dict) -> list:
    """
    Create fine-tuning examples from your Dakota dictionary.
    Each example teaches the model when and how to use the tool.
    """
    examples = []
    
    # Example 1: Simple translation
    examples.append({
        "messages": [
            {"role": "user", "content": "Translate 'water' to Dakota"},
            {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": "call_001",
                    "type": "function",
                    "function": {
                        "name": "dakota_lookup",
                        "arguments": json.dumps({
                            "word": "water",
                            "query_type": "english_to_dakota"
                        })
                    }
                }]
            },
            {
                "role": "tool",
                "content": json.dumps({
                    "english": "water",
                    "dakota": dakota_dict.get("water", "mni"),
                    "found": True
                }),
                "tool_call_id": "call_001"
            },
            {
                "role": "assistant",
                "content": f"The Dakota word for 'water' is **{dakota_dict.get('water', 'mni')}**."
            }
        ],
        "tools": [DAKOTA_DICTIONARY_TOOL]
    })
    
    # Add more examples for different scenarios:
    # - Reverse translation (Dakota to English)
    # - Definitions
    # - Usage examples
    # - Handling not found cases
    # - Multiple word queries
    
    return examples

# Save for fine-tuning
training_data = create_fine_tuning_examples(your_dakota_dict)
with open("dakota_finetuning.jsonl", "w") as f:
    for example in training_data:
        f.write(json.dumps(example) + "\n")
```

### Fine-Tuning Process

1. **Prepare your dataset** - Convert Dakota dictionary entries into conversation examples
2. **Include tool definitions** - Each example should include the tool schema
3. **Show tool usage patterns** - Teach when to use the tool vs. when to answer directly
4. **Upload to Moonshot** - Use their fine-tuning API to train a custom model
5. **Test the fine-tuned model** - Verify it correctly uses your Dakota tool

## Best Practices

### 1. Tool Description Quality
- **Be specific**: "Dakota language dictionary" not just "dictionary"
- **Include use cases**: When should Kimi use this tool?
- **Mention limitations**: What can't it do?

### 2. Parameter Design
- **Required vs Optional**: Only mark truly required parameters as required
- **Use enums**: For fixed sets of values (like query_type)
- **Descriptive names**: `word` not `w`, `query_type` not `qt`

### 3. Error Handling
- **Handle missing entries**: Return structured error responses
- **Validate inputs**: Check parameter types and values
- **Provide helpful errors**: "Word not found" with suggestions

### 4. Tool Response Format
- **Structured JSON**: Always return consistent structure
- **Include metadata**: `found: true/false`, `alternatives`, etc.
- **Rich information**: Include pronunciation, examples when available

## Integration with Existing Codebase

Your Dakota tool can be integrated into the existing `kimik2manim` architecture:

```python
# In a new file: dakota_tool.py
from typing import Dict, Any
import json
from ..kimi_client import KimiClient

class DakotaDictionaryTool:
    """Wrapper for Dakota dictionary tool."""
    
    def __init__(self, dictionary_path: str):
        self.dict = self._load_dictionary(dictionary_path)
        self.tool_def = self._create_tool_definition()
    
    def _load_dictionary(self, path: str) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _create_tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "dakota_lookup",
                "description": "...",
                "parameters": {
                    # ... your schema
                }
            }
        }
    
    def execute(self, word: str, query_type: str, **kwargs) -> dict:
        """Execute the actual lookup."""
        # Your implementation
        pass
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Return tool definition for API calls."""
        return self.tool_def
```

## Next Steps

1. **Examine your Dakota dictionary structure** - Understand the data format
2. **Design your tool schema** - Match your dictionary capabilities
3. **Implement the lookup function** - Actual code that uses your dictionary
4. **Test at inference time** - Verify tool calling works
5. **Create fine-tuning examples** - If you want to fine-tune
6. **Integrate into your workflow** - Use in your applications

## References

- [Kimi K2 Tool Calling Docs](https://platform.moonshot.ai/docs/guide/use-kimi-api-to-complete-tool-calls)
- [OpenAI Function Calling Format](https://platform.openai.com/docs/guides/function-calling)
- Your existing tool examples: `agents/enrichment_chain.py` (MATHEMATICAL_CONTENT_TOOL, etc.)

