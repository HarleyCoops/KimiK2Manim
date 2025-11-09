# KimiK2Manim

<div align="center">

<a href="https://github.com/HarleyCoops/KimiK2Manim/stargazers">
  <img alt="GitHub stars" src="https://img.shields.io/github/stars/HarleyCoops/KimiK2Manim?style=for-the-badge&logo=github&label=Star&color=gold">
</a>

![Rhombicosidodecahedron Animation](media/videos/render_rhombicosidodecahedron/480p15/partial_movie_files/ArtisticRhombicosidodecahedron/rhombicosidodecahedron_preview.gif)

*Rhombicosidodecahedron with 62 faces, golden ratio geometry, and dynamic multi-axis rotation*

</div>

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=HarleyCoops/KimiK2Manim&type=Date)](https://star-history.com/#HarleyCoops/KimiK2Manim&Date)

---

A standalone Python package for generating Manim animations using the **Kimi K2 thinking model** from Moonshot AI. This package provides agents that build knowledge trees, enrich them with mathematical content and visual specifications, and compose narrative prompts for Manim animation generation.

## Overview

KimiK2Manim uses the Kimi K2 model (via Moonshot AI's OpenAI-compatible API) to:

1. **Explore Prerequisites** - Build knowledge trees by identifying prerequisite concepts
2. **Enrich Mathematically** - Add LaTeX equations, definitions, and examples to each concept
3. **Design Visuals** - Plan Manim visual specifications (colors, animations, transitions)
4. **Compose Narratives** - Generate long-form animation prompts (2000+ words)

## Features

- **KimiClient**: OpenAI-compatible API wrapper for Moonshot AI
- **ToolAdapter**: Converts tool calls to verbose instructions when tools aren't available
- **KimiPrerequisiteExplorer**: Builds knowledge trees recursively
- **KimiEnrichmentPipeline**: Complete enrichment chain (math → visuals → narrative)
- **Standalone Package**: No dependencies on parent projects

## Agent Pipeline Flow

The KimiK2Manim pipeline consists of **4 sequential agents** that progressively enrich a knowledge tree until it contains everything needed to generate Manim animation code.

### Pipeline Stages

```
User Prompt → [Agent 1] → [Agent 2] → [Agent 3] → [Agent 4] → Manim Code
              Tree        Math        Visual      Narrative
```

#### Stage 1: Prerequisite Explorer (`KimiPrerequisiteExplorer`)

**Input**: User concept string (e.g., "pythagorean theorem")  
**Output**: `KnowledgeNode` tree with prerequisite structure

**Process**:
- Recursively explores prerequisite concepts
- Builds a hierarchical knowledge tree
- Each node contains: `concept`, `depth`, `is_foundation`, `prerequisites[]`

**Tool Calls**: Uses Kimi K2 to identify prerequisite concepts through natural language reasoning

#### Stage 2: Mathematical Enricher (`KimiMathematicalEnricher`)

**Input**: `KnowledgeNode` tree from Stage 1  
**Output**: Math-enriched tree with equations and definitions

**Process**:
- Recursively processes each node in the tree
- Adds mathematical content to each concept
- Enriches nodes with: `equations[]`, `definitions{}`, `interpretation`, `examples[]`, `typical_values{}`

**Tool Calls**: Uses `write_mathematical_content` tool to get structured math data:
```python
{
    "equations": ["a²+b²=c²", "c=√(a²+b²)"],
    "definitions": {"a": "length of leg", "b": "length of leg", "c": "hypotenuse"},
    "interpretation": "Geometric relationship in right triangles",
    "examples": ["3-4-5 triangle", "5-12-13 triangle"],
    "typical_values": {"3-4-5": "classic integer triangle"}
}
```

#### Stage 3: Visual Designer (`KimiVisualDesigner`)

**Input**: Math-enriched `KnowledgeNode` tree from Stage 2  
**Output**: Visual-enriched tree with Manim specifications

**Process**:
- Recursively designs visual specifications for each node
- Adds visual planning to `visual_spec` field
- Enriches with: `visual_description`, `color_scheme`, `animation_description`, `transitions`, `camera_movement`, `duration`, `layout`

**Tool Calls**: Uses `design_visual_plan` tool to get structured visual data:
```python
{
    "visual_description": "Right triangle with squares on each side",
    "color_scheme": "Blue, green, red for sides a, b, c",
    "animation_description": "Triangle draws itself, squares build outward",
    "transitions": "Fade in triangle first",
    "camera_movement": "Wide shot then zoom in",
    "duration": 15,
    "layout": "Center triangle with equation below"
}
```

#### Stage 4: Narrative Composer (`KimiNarrativeComposer`)

**Input**: Fully enriched `KnowledgeNode` tree (math + visuals) from Stage 3  
**Output**: Complete verbose narrative prompt (2000+ words)

**Process**:
- Orders nodes topologically (foundations first)
- Composes a single continuous narrative integrating all enrichments
- Creates final `narrative` field with verbose prompt

**Tool Calls**: Uses `compose_narrative` tool to generate the final prompt:
```python
{
    "verbose_prompt": "2000+ word narrative with LaTeX, visuals, timing...",
    "concept_order": ["foundation1", "foundation2", "target_concept"],
    "total_duration": 45,
    "scene_count": 3
}
```

### Tool Call Architecture

Each agent uses **Kimi K2's tool calling** to get structured data:

1. **Tool Definition**: Each agent defines a tool schema (function name, parameters, descriptions)
2. **API Call**: Agent sends tool definition to Kimi K2 with the task prompt
3. **Tool Response**: Kimi K2 returns structured JSON via function call
4. **Data Extraction**: Agent extracts JSON payload from `tool_calls[0].function.arguments`
5. **Fallback**: If tool call fails, falls back to parsing JSON from text response

**Example Tool Call Flow**:
```python
# Agent sends request with tool definition
response = client.chat_completion(
    messages=[{"role": "user", "content": "Enrich pythagorean theorem"}],
    tools=[MATHEMATICAL_CONTENT_TOOL],
    tool_choice="auto"
)

# Extract structured data from tool call
tool_calls = response["choices"][0]["message"]["tool_calls"]
payload = json.loads(tool_calls[0]["function"]["arguments"])
# payload = {"equations": [...], "definitions": {...}, ...}
```

### API Call Implementation Details

KimiK2Manim uses the **OpenAI-compatible API** from Moonshot AI to communicate with the Kimi K2 thinking model:

#### KimiClient Architecture

The [KimiClient](kimi_client.py) class wraps the OpenAI Python SDK:

```python
from openai import OpenAI

class KimiClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        self.client = OpenAI(
            api_key=api_key or MOONSHOT_API_KEY,
            base_url=base_url or "https://api.moonshot.cn/v1"
        )
        self.model = model or "kimi-k2-0905-preview"
```

#### API Call Features

1. **Tool Calling Support**: The client supports OpenAI-compatible function calling
   - Tools defined in JSON schema format
   - Automatic extraction of structured responses
   - Fallback to text parsing if tool calls fail

2. **Response Formatting**: Converts OpenAI SDK responses to consistent dict format
   - Extracts message content, tool calls, and usage statistics
   - Handles streaming and non-streaming responses

3. **Error Handling**: Provides detailed authentication and API error messages
   - 401 authentication troubleshooting
   - API key validation
   - Endpoint verification

4. **Logging**: Built-in verbose logging for debugging
   - API request details (messages, tokens, tools)
   - Response metadata (token usage, content length)
   - Tool call information (function names, arguments)

#### Tool Definition Structure

Each agent defines tools using OpenAI's function calling schema:

```python
MATHEMATICAL_CONTENT_TOOL = {
    "type": "function",
    "function": {
        "name": "write_mathematical_content",
        "description": "Return key mathematical information...",
        "parameters": {
            "type": "object",
            "properties": {
                "equations": {
                    "type": "array",
                    "description": "2-5 LaTeX strings",
                    "items": {"type": "string"}
                },
                "definitions": {
                    "type": "object",
                    "description": "Symbol to definition mapping",
                    "additionalProperties": {"type": "string"}
                }
                # ... more properties
            },
            "required": ["equations", "definitions"]
        }
    }
}
```

#### ToolAdapter for Non-Tool Mode

The [ToolAdapter](tool_adapter.py) converts tool definitions to natural language instructions when tool calling is unavailable:

```python
from kimik2manim.tool_adapter import ToolAdapter

adapter = ToolAdapter()
instructions = adapter.tools_to_instructions([MATHEMATICAL_CONTENT_TOOL])
# Converts tool schema to verbose prompt instructions
```

This allows the pipeline to work even if the API doesn't support function calling.

#### API Call Example from Enrichment Pipeline

From [enrichment_chain.py:199-207](agents/enrichment_chain.py#L199-L207):

```python
response = self.client.chat_completion(
    messages=[{"role": "user", "content": user_prompt}],
    system=system_prompt,
    tools=[MATHEMATICAL_CONTENT_TOOL],
    tool_choice="auto",
    max_tokens=1200,
    temperature=0.2,
)

payload = _extract_tool_payload(response)
if payload is None:
    payload = _parse_json_fallback(self.client.get_text_content(response))
```

The enrichment agents make API calls with:
- **Structured system prompts** describing the agent's role
- **User prompts** with concept details and enrichment requirements
- **Tool definitions** specifying expected JSON structure
- **Fallback parsing** if structured tool calls aren't returned

### Progressive Enrichment

The `KnowledgeNode` tree gets progressively enriched at each stage:

```
Initial Tree:
  - concept
  - depth
  - prerequisites[]

After Math Enrichment:
  + equations[]
  + definitions{}
  + interpretation
  + examples[]

After Visual Enrichment:
  + visual_spec.visual_description
  + visual_spec.color_scheme
  + visual_spec.animation_description
  + visual_spec.duration
  + ...

After Narrative Composition:
  + narrative (verbose_prompt)
```

### Final Output

The enriched tree contains everything needed for Manim code generation:
- **Equations**: LaTeX strings ready for `MathTex()`
- **Visual Specs**: Complete descriptions of what to animate
- **Narrative**: 2000+ word prompt with timing, transitions, and scene flow
- **Structure**: Prerequisite ordering ensures logical presentation

This enriched data can then be used to generate complete Manim Python code that renders the animation.

## Installation

### From Source

```bash
git clone https://github.com/HarleyCoops/KimiK2Manim.git
cd KimiK2Manim
pip install -e .
```

### Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `openai>=1.0.0` - OpenAI-compatible API client
- `python-dotenv>=1.0.0` - Environment variable management

## Quick Start

### 1. Get API Key

Register at [Moonshot AI Platform](https://platform.moonshot.ai/) and get your API key.

### 2. Set Environment Variable

Create a `.env` file in the project root:

```bash
MOONSHOT_API_KEY=your_api_key_here
KIMI_MODEL=kimi-k2-0905-preview  # Optional: specify model name (Kimi K2 model)
KIMI_USE_TOOLS=true        # Optional: enable/disable tools
KIMI_ENABLE_THINKING=heavy  # Optional: thinking mode - "heavy" (max reasoning), "medium", "light", or "true"/"false"
```

### 3. Basic Usage

```python
from kimik2manim.agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer
import asyncio

async def main():
    explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True)
    tree = await explorer.explore_async("quantum field theory", verbose=True)
    tree.print_tree()
    
    # Save to JSON
    import json
    with open("tree.json", "w") as f:
        json.dump(tree.to_dict(), f, indent=2)

asyncio.run(main())
```

### 4. Run Enrichment Pipeline

```python
from kimik2manim.agents.enrichment_chain import KimiEnrichmentPipeline
from kimik2manim.agents.prerequisite_explorer_kimi import KnowledgeNode
import json
import asyncio

async def main():
    # Load existing tree (or create one)
    with open("tree.json", "r") as f:
        tree_data = json.load(f)
    
    # Convert to KnowledgeNode (simplified - see examples for full implementation)
    tree = KnowledgeNode(**tree_data)  # Adjust based on your structure
    
    # Run enrichment
    pipeline = KimiEnrichmentPipeline()
    result = await pipeline.run_async(tree)
    
    # Access enriched data
    print(f"Narrative length: {len(result.narrative.verbose_prompt)} characters")
    print(f"Total duration: {result.narrative.total_duration}s")

asyncio.run(main())
```

### 5. Command-Line Usage

```bash
# Run enrichment pipeline on a tree JSON file
python examples/run_enrichment_pipeline.py path/to/tree.json
```

## Example Renderings

### Rhombicosidodecahedron Animation

KimiK2Manim has been used to generate stunning 3D visualizations, including this rhombicosidodecahedron animation:

The rhombicosidodecahedron is an Archimedean solid with:
- **62 faces**: 20 triangles, 30 squares, and 12 pentagons
- **60 vertices** positioned using golden ratio-based coordinates
- **120 edges** connecting the vertices

#### Visual Design Features

The animation ([manim_scenes/render_rhombicosidodecahedron.py](manim_scenes/render_rhombicosidodecahedron.py)) showcases:

- **Color-coded face types**:
  - Gold edges for pentagonal faces
  - Blue edges for square faces
  - Red edges for triangular faces
- **Glowing vertices** with multi-layer halos
- **Dynamic rotation** on multiple axes with time-varying rotation vector
- **Gradient background** with deep space aesthetic
- **Smooth camera movements** and zoom effects

#### Enhanced Epic Version

The [manim_scenes/epic_rhombicosidodecahedron.py](manim_scenes/epic_rhombicosidodecahedron.py) includes additional effects:

- **Starfield background** with 100 animated stars
- **Enhanced glow effects** on edges and vertices
- **Dynamic camera orbits** with zoom in/out sequences
- **Multi-layered vertex halos** (outer, middle, core)
- **Smooth fade in/out transitions**
- **Title overlay** with golden text

#### Mathematical Formulation

The vertex coordinates use golden ratio constants from McCooey's data:

```python
C0 = (1 + √5) / 4
C1 = (3 + √5) / 4
C2 = (1 + √5) / 2  # Golden ratio φ
C3 = (5 + √5) / 4
C4 = (2 + √5) / 2
```

Vertices are positioned in 3D space using combinations of these constants, creating the precise geometry of the rhombicosidodecahedron.

#### Rendering the Animation

To render the rhombicosidodecahedron:

```bash
# Basic version
manim -pql manim_scenes/render_rhombicosidodecahedron.py ArtisticRhombicosidodecahedron

# Epic version with enhanced effects
manim -pql manim_scenes/epic_rhombicosidodecahedron.py EpicRhombicosidodecahedron

# High quality render
manim -pqh manim_scenes/epic_rhombicosidodecahedron.py EpicRhombicosidodecahedron
```

### Harmonic Division Theorem Animation

<div align="center">

![Harmonic Theorem Animation](media/videos/harmonic_theorem/480p15/harmonic_theorem_preview.gif)

*45-second demonstration of the Harmonic Division Theorem with step-by-step LaTeX equations*

</div>

The Harmonic Division Theorem animation demonstrates a fundamental concept in projective geometry:

**Mathematical Concept**: Points A, C, D, B are in harmonic division if their cross-ratio equals -1:
```
(A,B;C,D) = (AC·BD)/(BC·AD) = -1
```

#### Animation Structure (45 seconds)

The animation ([manim_scenes/harmonic_theorem.py](manim_scenes/harmonic_theorem.py)) presents the theorem in five acts:

1. **Introduction (0-5s)**: Title and geometric setup
2. **Construction (5-15s)**: Four collinear points with harmonic division property
3. **Cross-Ratio (15-28s)**: Step-by-step calculation with color-coded segments
4. **Visual Proof (28-40s)**: Circle construction showing harmonic conjugates
5. **Conclusion (40-45s)**: Final boxed theorem

#### Visual Design Features

- **Color-coded points**: A (BLUE), C (GOLD), D (RED), B (GREEN)
- **Glowing halos** around points for emphasis
- **Sequential LaTeX equations** revealed step-by-step
- **Segment highlighting** showing AC·BD and BC·AD relationships
- **Geometric circle** demonstrating pole-polar duality
- **Dark gradient background** for professional aesthetic

#### Rendering the Animation

```bash
# Preview quality
manim -pql manim_scenes/harmonic_theorem.py HarmonicDivisionTheorem

# High quality render
manim -pqh manim_scenes/harmonic_theorem.py HarmonicDivisionTheorem
```

The animation was generated using the KimiK2Manim enrichment pipeline, which:
1. Explored prerequisites (cross-ratio, collinear points, harmonic conjugates)
2. Enriched with LaTeX equations and definitions
3. Designed visual specifications (colors, animations, timing)
4. Composed a narrative prompt with exact 45-second timing breakdown

See [manim_scenes/README.md](manim_scenes/README.md) for more rendering examples and all available scenes.

This demonstrates how KimiK2Manim can be used to generate complex mathematical visualizations with artistic flair!

## Project Structure

```
KimiK2Manim/
├── README.md                    # This file
├── setup.py                     # Package setup
├── requirements.txt             # Dependencies
├── .gitignore                   # Git ignore rules
├── config.py                    # Configuration and constants
├── kimi_client.py               # Kimi K2 API client wrapper
├── tool_adapter.py              # Tool call to verbose instruction converter
│
├── agents/                      # Core AI agents
│   ├── __init__.py
│   ├── prerequisite_explorer_kimi.py  # Knowledge tree builder
│   └── enrichment_chain.py     # Math, visual, narrative enrichment
│
├── manim_scenes/                # Manim animation scripts
│   ├── README.md               # Scene documentation
│   ├── render_rhombicosidodecahedron.py
│   ├── epic_rhombicosidodecahedron.py
│   ├── enhance_rhombicosidodecahedron.py
│   ├── kimi2pythag.py
│   └── Kimik2First.py
│
├── examples/                    # Example usage and test scripts
│   ├── test_kimi_integration.py
│   ├── run_enrichment_pipeline.py
│   ├── test_qft_pipeline.py
│   ├── run_pipeline.py
│   ├── test_pipeline_debug.py
│   └── test_pipeline_simple.py
│
├── output/                      # Generated outputs
│   └── rhombicosidodecahedron_narrative.txt
│
├── media/                       # Manim rendered videos
│   └── videos/
│
├── docs/                        # Documentation
│   └── ARCHITECTURE.md
│
└── dev/                         # Development and experimental files
    ├── KimiChatRhom.py
    └── textprompt.txt
```

## Configuration

All configuration is in `config.py` or via environment variables:

- `MOONSHOT_API_KEY`: Your Moonshot AI API key (required)
- `KIMI_MODEL`: Kimi K2 model name (default: "kimi-k2-0905-preview")
- `KIMI_USE_TOOLS`: Enable tool calling (default: "true")
- `KIMI_ENABLE_THINKING`: Thinking mode - "heavy" (max reasoning), "medium", "light", or "true"/"false" (default: "true")

## Key Components

### KimiClient

OpenAI-compatible wrapper for Moonshot AI's API:

```python
from kimik2manim.kimi_client import KimiClient

client = KimiClient()
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)
print(client.get_text_content(response))
```

### ToolAdapter

Converts tool definitions to verbose instructions:

```python
from kimik2manim.tool_adapter import ToolAdapter

adapter = ToolAdapter()
tools = [...]  # Your tool definitions
instructions = adapter.tools_to_instructions(tools)
```

### KimiPrerequisiteExplorer

Builds knowledge trees by exploring prerequisites:

```python
from kimik2manim.agents.prerequisite_explorer_kimi import KimiPrerequisiteExplorer

explorer = KimiPrerequisiteExplorer(max_depth=3, use_tools=True)
tree = await explorer.explore_async("special relativity", verbose=True)
```

### KimiEnrichmentPipeline

Complete enrichment chain:

```python
from kimik2manim.agents.enrichment_chain import KimiEnrichmentPipeline

pipeline = KimiEnrichmentPipeline()
result = await pipeline.run_async(tree)
```

## Examples

See the `examples/` directory for:
- `test_kimi_integration.py` - Basic API and agent tests
- `run_enrichment_pipeline.py` - CLI for running enrichment
- `test_qft_pipeline.py` - Full pipeline test with QFT concepts

## Testing

```bash
# Run tests (requires MOONSHOT_API_KEY)
pytest tests/ -v

# Run without API calls (unit tests only)
pytest tests/ -v -k "not api"
```

## Architecture

The package follows a layered architecture with agent orchestration:

1. **Client Layer**: `KimiClient` handles all API communication with Moonshot AI
2. **Adapter Layer**: `ToolAdapter` converts tool calls to verbose instructions when tools aren't available
3. **Agent Layer**: 4 sequential agents orchestrate knowledge tree building and enrichment
4. **Orchestrator**: `KimiEnrichmentPipeline` coordinates the 3 enrichment agents

### Agent Orchestration

The `KimiEnrichmentPipeline` orchestrator runs agents in sequence:

```python
async def run_async(self, root: KnowledgeNode) -> EnrichmentResult:
    # Stage 2: Math enrichment (recursive)
    await self.math.enrich_tree(root)
    
    # Stage 3: Visual design (recursive)
    await self.visual.design_tree(root)
    
    # Stage 4: Narrative composition
    narrative = await self.narrative.compose_async(root)
    
    return EnrichmentResult(enriched_tree=root, narrative=narrative)
```

Each agent processes the entire tree recursively, ensuring all nodes (including prerequisites) are enriched before moving to the next stage.

See `docs/ARCHITECTURE.md` for detailed architecture documentation.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [Moonshot AI Platform](https://platform.moonshot.ai/)
- [Kimi K2 Documentation](https://platform.moonshot.ai/docs/guide/use-kimi-k2-thinking-model)
- [Manim Documentation](https://docs.manim.community/)

## Support

For issues and questions, please open an issue on [GitHub](https://github.com/HarleyCoops/KimiK2Manim/issues).
