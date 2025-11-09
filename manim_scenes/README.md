# Manim Animation Scenes

This directory contains Manim animation scripts that demonstrate mathematical visualizations generated using KimiK2Manim.

## Available Scenes

### Rhombicosidodecahedron Animations

#### 1. Artistic Rhombicosidodecahedron
**File:** [render_rhombicosidodecahedron.py](render_rhombicosidodecahedron.py)

Basic artistic rendering with:
- Color-coded edges by face type (gold, blue, red)
- Glowing vertices with halos
- Dynamic multi-axis rotation
- Gradient background

**Render:**
```bash
manim -pql render_rhombicosidodecahedron.py ArtisticRhombicosidodecahedron
```

#### 2. Epic Rhombicosidodecahedron
**File:** [epic_rhombicosidodecahedron.py](epic_rhombicosidodecahedron.py)

Enhanced version with:
- Starfield background (100 animated stars)
- Enhanced glow effects
- Dynamic camera orbits and zoom sequences
- Multi-layered vertex halos
- Title overlay

**Render:**
```bash
manim -pql epic_rhombicosidodecahedron.py EpicRhombicosidodecahedron
```

#### 3. Enhanced Rhombicosidodecahedron
**File:** [enhance_rhombicosidodecahedron.py](enhance_rhombicosidodecahedron.py)

Advanced version with additional mathematical annotations and effects.

### Other Scenes

#### Pythagorean Theorem
**File:** [kimi2pythag.py](kimi2pythag.py)

Visualization of the Pythagorean theorem.

#### First Demo
**File:** [Kimik2First.py](Kimik2First.py)

Initial demonstration scene.

## Rendering Guide

### Quality Levels

- **Low Quality (preview):** `-ql` - Fast rendering for testing
- **Medium Quality:** `-qm` - Balanced quality and speed
- **High Quality:** `-qh` - Full quality for final output
- **4K Quality:** `-qk` - Ultra high resolution

### Common Commands

```bash
# Preview at low quality
manim -pql <script.py> <SceneName>

# High quality render
manim -pqh <script.py> <SceneName>

# Render without playing
manim -qh <script.py> <SceneName>

# List all scenes in a file
manim <script.py>
```

## Output Location

Rendered videos are saved to: `../media/videos/<script_name>/<quality>/`
