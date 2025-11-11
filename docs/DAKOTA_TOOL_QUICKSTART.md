# Dakota Dictionary Tool - Quick Reference

## Overview

This guide helps you convert a Dakota dictionary into a custom tool for Kimi K2 API that can be used:
- **At inference time** - Tools are called dynamically during conversations
- **During fine-tuning** - Tool usage patterns are learned from training examples

## Quick Start

### 1. Analyze Your Dictionary

```bash
python utils/convert_dakota_to_tool.py your_dakota_dict.json --output-tool dakota_tool.json
```

This will:
- Analyze your dictionary structure
- Generate a tool definition JSON schema
- Create a Python implementation template

### 2. Use the Tool at Inference

See `examples/dakota_tool_example.py` for a complete working example:

```python
from kimik2manim.kimi_client import get_kimi_client

client = get_kimi_client()
response = client.chat_completion(
    messages=[{"role": "user", "content": "What is 'water' in Dakota?"}],
    tools=[DAKOTA_TOOL_DEFINITION],
    tool_choice="auto"
)
```

### 3. Create Fine-Tuning Data (Optional)

```bash
python utils/convert_dakota_to_tool.py your_dakota_dict.json \
    --output-finetuning dakota_finetuning.jsonl \
    --num-examples 50
```

## Tool Definition Format

Kimi uses OpenAI-compatible function calling format:

```python
{
    "type": "function",
    "function": {
        "name": "dakota_lookup",
        "description": "Look up words in Dakota dictionary...",
        "parameters": {
            "type": "object",
            "properties": {
                "word": {"type": "string"},
                "query_type": {"type": "string", "enum": [...]}
            },
            "required": ["word", "query_type"]
        }
    }
}
```

## How It Works

### At Inference Time

1. **User asks question** → "What is 'water' in Dakota?"
2. **Kimi decides to use tool** → Calls `dakota_lookup(word="water", query_type="english_to_dakota")`
3. **Your code executes** → Looks up in your dictionary, returns `{"dakota": "mni"}`
4. **Kimi receives result** → Formats final answer: "The Dakota word for 'water' is **mni**"

### During Fine-Tuning

Training examples teach Kimi:
- **When** to use the tool (Dakota-related questions)
- **How** to format tool calls (correct parameters)
- **How** to interpret results (use tool output in answer)

## Files Created

- `docs/DAKOTA_TOOL_GUIDE.md` - Comprehensive guide
- `examples/dakota_tool_example.py` - Working example code
- `utils/convert_dakota_to_tool.py` - Dictionary conversion utility

## Key Concepts

### Tool Schema Design
- **Name**: Clear, descriptive function name
- **Description**: Tells Kimi when to use the tool
- **Parameters**: JSON Schema defining inputs
- **Required fields**: Only mark truly required parameters

### Tool Execution Flow
1. Define tool schema
2. Include in API call (`tools=[...]`)
3. Kimi returns tool call request
4. Execute your function with provided arguments
5. Send results back to Kimi
6. Kimi generates final answer

### Fine-Tuning Format
Each training example includes:
- User message
- Assistant tool call
- Tool execution result
- Final assistant response
- Tool definition

## Next Steps

1. **Examine your dictionary** - Understand its structure
2. **Run the converter** - Generate tool definition
3. **Test at inference** - Use `dakota_tool_example.py`
4. **Create fine-tuning data** - If you want to fine-tune
5. **Integrate into your app** - Use in production

## References

- Full guide: `docs/DAKOTA_TOOL_GUIDE.md`
- Example code: `examples/dakota_tool_example.py`
- Existing tools: `agents/enrichment_chain.py` (MATHEMATICAL_CONTENT_TOOL, etc.)
- Kimi docs: https://platform.moonshot.ai/docs/guide/use-kimi-api-to-complete-tool-calls

