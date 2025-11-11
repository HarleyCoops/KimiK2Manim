# Learning Path: KimiK2Manim Codebase

This guide will help you understand the codebase step-by-step, starting with the fundamentals.

## Recommended Learning Order

### **Step 1: Foundation - Configuration & Setup** (15 minutes)
**Files to read:**
- `config.py` - Configuration system (API keys, model settings, defaults)
- `docs/SETUP.md` - Setup instructions

**What you'll learn:**
- How configuration is loaded from environment variables
- What settings control the behavior
- How to set up your API key

**Action:** Read `config.py` and understand each configuration option.

---

### **Step 2: Core - API Client** (30 minutes)
**Files to read:**
- `kimi_client.py` - The HTTP client wrapper (lines 41-280)
- `e2b_sandbox/test_kimi_api.py` - Simple test example

**What you'll learn:**
- How `KimiClient` wraps the OpenAI SDK
- How API calls are made (no model weights downloaded!)
- Response format and how to extract text
- The singleton pattern (`get_kimi_client()`)

**Key concepts:**
```python
# This creates an HTTP client, NOT a model
client = KimiClient()

# This makes an HTTP request to Moonshot servers
response = client.chat_completion(messages=[...])

# Extract the generated text
text = client.get_text_content(response)
```

**Action:** 
1. Read `kimi_client.py` focusing on `__init__` and `chat_completion` methods
2. Run `python e2b_sandbox/test_kimi_api.py` to see it in action

---

### **Step 3: Understanding - Tool Adapter** (20 minutes)
**Files to read:**
- `tool_adapter.py` - Converts tool calls to verbose instructions
- `examples/test_kimi_integration.py` - `test_tool_adapter()` function (lines 79-121)

**What you'll learn:**
- Why tools might not be available
- How tool definitions are converted to natural language
- The fallback mechanism for when tools aren't supported

**Key concept:** Some APIs don't support function calling, so tools are converted to verbose instructions that achieve the same goal.

**Action:** Read `tool_adapter.py` and understand `tool_to_instruction()` method.

---

### **Step 4: Data Structure - KnowledgeNode** (15 minutes)
**Files to read:**
- `agents/prerequisite_explorer_kimi.py` - `KnowledgeNode` class (lines 34-83)

**What you'll learn:**
- The core data structure that represents concepts
- How knowledge trees are built recursively
- What fields get added during enrichment

**Key structure:**
```python
@dataclass
class KnowledgeNode:
    concept: str                    # "pythagorean theorem"
    depth: int                      # 0, 1, 2...
    is_foundation: bool            # True if foundational concept
    prerequisites: List[...]        # Child nodes
    equations: Optional[List[str]]  # Added by math enricher
    definitions: Optional[Dict]    # Added by math enricher
    visual_spec: Optional[Dict]    # Added by visual designer
    narrative: Optional[str]       # Added by narrative composer
```

**Action:** Read the `KnowledgeNode` class and understand `to_dict()` and `print_tree()` methods.

---

### **Step 5: First Agent - Prerequisite Explorer** (45 minutes)
**Files to read:**
- `agents/prerequisite_explorer_kimi.py` - Main agent (lines 86-440)
- `examples/test_kimi_integration.py` - `test_prerequisite_explorer()` (lines 53-76)

**What you'll learn:**
- How agents interact with the API
- Recursive tree building
- How prerequisites are discovered
- The async/await pattern used throughout

**Key flow:**
```
User concept → API call → Parse response → Build node → 
Recurse for prerequisites → Build tree
```

**Action:**
1. Read `KimiPrerequisiteExplorer.explore_async()` method
2. Run `python examples/test_kimi_integration.py` and focus on Test 2
3. Trace through one concept exploration manually

---

### **Step 6: Pipeline - Full Enrichment Chain** (30 minutes)
**Files to read:**
- `agents/enrichment_chain.py` - The complete pipeline
- `examples/test_pipeline_simple.py` - Simple pipeline example

**What you'll learn:**
- How the 4-stage pipeline works:
  1. Prerequisite Explorer (builds tree)
  2. Mathematical Enricher (adds equations)
  3. Visual Designer (adds visual specs)
  4. Narrative Composer (creates final prompt)

**Key concept:** Each stage enriches the same `KnowledgeNode` tree with more information.

**Action:** Read `KimiEnrichmentPipeline` class and understand the flow.

---

### **Step 7: Examples - See It All Together** (30 minutes)
**Files to read:**
- `examples/test_kimi_integration.py` - Complete test suite
- `examples/run_pipeline.py` - Full pipeline example
- `examples/test_pipeline_simple.py` - Simplified example

**What you'll learn:**
- How everything fits together
- Common patterns and error handling
- How to use the pipeline in your own code

**Action:** Run the examples and modify them to explore different concepts.

---

## Quick Reference: Key Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `config.py` | Configuration | First - understand settings |
| `kimi_client.py` | API client | Second - core communication |
| `tool_adapter.py` | Tool conversion | Third - understand fallbacks |
| `agents/prerequisite_explorer_kimi.py` | First agent | Fourth - see agent pattern |
| `agents/enrichment_chain.py` | Full pipeline | Fifth - see complete flow |
| `examples/test_kimi_integration.py` | Examples | Sixth - see usage |

---

## Understanding the Architecture

### The Flow:
```
User Input
    ↓
[1] Prerequisite Explorer → KnowledgeNode Tree
    ↓
[2] Mathematical Enricher → Tree + Equations
    ↓
[3] Visual Designer → Tree + Visual Specs
    ↓
[4] Narrative Composer → Tree + Narrative
    ↓
Final Enriched Tree → Manim Code Generation
```

### Key Design Patterns:
1. **API Client Pattern**: `KimiClient` wraps HTTP requests
2. **Singleton Pattern**: `get_kimi_client()` for efficiency
3. **Tool Adapter Pattern**: Fallback from tools to verbose instructions
4. **Recursive Processing**: Agents process trees recursively
5. **Progressive Enrichment**: Each stage adds more data to the same tree

---

## Tips for Learning

1. **Start Small**: Begin with `test_kimi_api.py` - just API calls
2. **Add Complexity Gradually**: Move from API → Tool Adapter → Agent → Pipeline
3. **Read Tests**: The test files show how things are actually used
4. **Trace Execution**: Pick a simple concept and trace through the code
5. **Modify Examples**: Change the examples to see what happens

---

## Next Steps After Basics

Once you understand the basics:
1. Explore `agents/enrichment_chain.py` - see how agents chain together
2. Look at `manim_scenes/` - see how narratives become animations
3. Check `e2b_sandbox/` - sandbox-specific utilities
4. Read `docs/ARCHITECTURE.md` - deeper architectural details

---

## Common Questions

**Q: Where does the actual model run?**  
A: On Moonshot AI servers. Your code only makes HTTP requests. See `e2b_sandbox/KIMI_API_ARCHITECTURE.md`.

**Q: How do I add a new agent?**  
A: Follow the pattern in `prerequisite_explorer_kimi.py` - inherit from base patterns, use `KimiClient`, handle tools/verbose fallback.

**Q: How do I debug API calls?**  
A: Check `logger.py` - it logs all API calls with details. Set verbose mode for more output.

**Q: What's the difference between tools and verbose mode?**  
A: Tools = structured function calls. Verbose = natural language instructions. `ToolAdapter` converts between them.

---

## Exercises

1. **Exercise 1**: Modify `test_kimi_api.py` to ask a different question
2. **Exercise 2**: Create a simple script that explores prerequisites for "quantum mechanics"
3. **Exercise 3**: Trace through one API call and print what gets sent/received
4. **Exercise 4**: Modify the pipeline to stop after math enrichment (skip visual/narrative)
5. **Exercise 5**: Add a new field to `KnowledgeNode` and update the enrichment chain

Start with Step 1 and work your way through. Each step builds on the previous one!

