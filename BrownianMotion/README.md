# Brownian Motion and Einstein's Heat Equation

This directory contains a complete example of using the KimiK2Manim pipeline to generate a 2-minute educational animation on Brownian Motion and its connection to Einstein's Heat Equation.

## Overview

The Brownian Motion project demonstrates:
- **Full pipeline integration**: From concept exploration to final Manim scene
- **Frame boundary solutions**: Three scene versions showing different constraint approaches
- **Scene management**: Automatic text/equation lifecycle management
- **Educational content**: Complete 2-minute animation with mathematical rigor

## Files

### Pipeline Scripts

- **`run_pipeline.py`** - Main pipeline script that:
  - Explores prerequisites for "Brownian Motion and Einstein's Heat Equation"
  - Enriches the knowledge tree with mathematics and visual specifications
  - Generates narrative prompts
  - Saves enriched JSON and narrative text files

### Manim Scene Scripts

1. **`brownian_motion_scene.py`** - Original unbounded scene
   - Basic implementation without constraints
   - Manual text positioning
   - Good for understanding the core concepts

2. **`brownian_motion_bounded.py`** - Bounded scene with frame constraints
   - Uses `BoundedScene` base class from `manim_utils`
   - All content automatically constrained within safe boundaries
   - Prevents content from rendering outside visible area
   - Demonstrates frame boundary solution

3. **`brownian_motion_managed.py`** - Complete managed scene (Recommended)
   - Uses `ManagedBoundedScene` combining both systems
   - Automatic text/equation lifecycle management
   - Zone-based positioning prevents overlaps
   - Clean section transitions
   - Best practice implementation

### Output Files

- **`output/Brownian_Motion_and_Einstein's_Heat_Equation_prerequisite_tree.json`**
  - Initial knowledge tree from prerequisite exploration
  - Contains concept hierarchy and prerequisites

- **`output/Brownian_Motion_and_Einstein's_Heat_Equation_enriched.json`**
  - Fully enriched knowledge tree
  - Includes equations, definitions, visual specs, and narrative
  - Used as input for Manim scene generation

- **`output/Brownian_Motion_and_Einstein's_Heat_Equation_narrative.txt`**
  - Verbose narrative prompt (2000+ words)
  - Complete animation description with timing

## Running the Pipeline

### Step 1: Generate Enriched Content

```bash
cd BrownianMotion
python run_pipeline.py
```

This will:
1. Explore prerequisites for "Brownian Motion and Einstein's Heat Equation"
2. Enrich with mathematical content (equations, definitions)
3. Design visual specifications
4. Compose narrative prompt
5. Save outputs to `output/` directory

### Step 2: Render the Animation

```bash
# Recommended: Managed scene with all features
python -m manim -pql brownian_motion_managed.py BrownianMotionManaged

# Bounded scene (frame constraints only)
python -m manim -pql brownian_motion_bounded.py BrownianMotionBounded

# Original scene (no constraints)
python -m manim -pql brownian_motion_scene.py BrownianMotionAndEinsteinHeatEquation

# High quality render
python -m manim -pqh brownian_motion_managed.py BrownianMotionManaged
```

## Animation Structure

The 2-minute (120 second) animation is divided into 6 sections:

1. **Introduction (0-15s)**
   - Title: "Brownian Motion and Einstein's Heat Equation"
   - Historical context: Einstein's 1905 work

2. **Microscopic View (15-45s)**
   - 200 water molecules (blue dots) moving randomly
   - 5 pollen grains (golden spheres) with colored trajectory trails
   - Demonstrates Brownian motion visually

3. **Random Walk Analysis (45-70s)**
   - Animated random walk trajectory
   - Mean squared displacement graph
   - Equation: `⟨x²(t)⟩ = 2Dt`

4. **Diffusion Equation (70-95s)**
   - PDE: `∂P/∂t = D∇²P`
   - Gaussian solution visualization
   - Probability distribution spreading

5. **Einstein's Relation (95-115s)**
   - Stokes-Einstein: `D = k_B T / (6πηa)`
   - Connection to heat equation
   - Mathematical structure comparison

6. **Conclusion (115-120s)**
   - Summary message

## Mathematical Concepts

The animation covers:

- **Random Walk Theory**: Unpredictable particle motion
- **Mean Squared Displacement**: `⟨x²(t)⟩ = 2Dt` (linear growth)
- **Diffusion Equation**: `∂P/∂t = D∇²P` (probability spreading)
- **Gaussian Solution**: `P(x,t|x₀,0) = (1/√(4πDt)) exp[-(x-x₀)²/(4Dt)]`
- **Einstein's Relation**: `D = k_B T / (6πηa)` (microscopic to macroscopic)
- **Heat Equation Connection**: `∂u/∂t = α∇²u` (same mathematical structure)

## Frame Boundary Solutions

This project demonstrates solutions to universal Manim rendering issues:

### Problem 1: Content Renders Outside Frame

**Solution**: `BoundedScene` base class
- Automatically constrains all content within safe boundaries
- Safe area: 12.78 × 7.2 units (90% of full frame)
- Methods: `bounded_text()`, `bounded_math_tex()`, `create_safe_axes()`

See: [`../manim_utils/README_BOUNDED_SCENE.md`](../manim_utils/README_BOUNDED_SCENE.md)

### Problem 2: Text/Equations Overlap

**Solution**: `ManagedBoundedScene` with scene management
- Automatic text/equation lifecycle management
- Zone-based positioning (title, equation, explanation zones)
- Old content automatically fades out when new content is added
- Methods: `add_title()`, `add_explanation()`, `add_equation()`, `transition_section()`

See: [`../manim_utils/README_SCENE_MANAGEMENT.md`](../manim_utils/README_SCENE_MANAGEMENT.md)

## Usage Examples

### Using ManagedBoundedScene

```python
from manim_utils.managed_scene import ManagedBoundedScene

class MyScene(ManagedBoundedScene):
    def construct(self):
        # Title automatically replaces previous titles
        title = self.add_title("My Title")
        self.play(Write(title))
        
        # Explanation automatically replaces previous explanations
        explanation = self.add_explanation("This explains something")
        self.play(FadeIn(explanation))
        
        # Equation automatically replaces previous equations
        eq = self.add_equation(r"E = mc^2")
        self.play(Write(eq))
        
        # Transition to new section (clears old content)
        self.transition_section("New Section Title")
```

### Using BoundedScene

```python
from manim_utils.bounded_scene import BoundedScene

class MyScene(BoundedScene):
    def construct(self):
        # Text automatically scales to fit
        title = self.bounded_text("My Title", font_size=48)
        self.safe_position(title, position='top')
        
        # Equation automatically scales to fit
        eq = self.bounded_math_tex(r"x^2 + y^2 = r^2", font_size=60)
        self.safe_position(eq, position='center')
        
        # Axes automatically fit within boundaries
        axes = self.create_safe_axes(x_range=(-5, 5, 1), y_range=(-3, 3, 1))
```

## Output Location

Rendered videos are saved to:
```
BrownianMotion/media/videos/brownian_motion_managed/480p15/BrownianMotionManaged.mp4
BrownianMotion/media/videos/brownian_motion_bounded/480p15/BrownianMotionBounded.mp4
BrownianMotion/media/videos/brownian_motion_scene/480p15/BrownianMotionAndEinsteinHeatEquation.mp4
```

## References

- [Einstein's 1905 Paper on Brownian Motion](https://en.wikipedia.org/wiki/Einstein_relation_(kinetic_theory))
- [Stokes-Einstein Relation](https://en.wikipedia.org/wiki/Einstein_relation_(kinetic_theory))
- [Diffusion Equation](https://en.wikipedia.org/wiki/Diffusion_equation)
- [Heat Equation](https://en.wikipedia.org/wiki/Heat_equation)

## Related Documentation

- [`../manim_utils/README_BOUNDED_SCENE.md`](../manim_utils/README_BOUNDED_SCENE.md) - Frame boundary constraints
- [`../manim_utils/README_SCENE_MANAGEMENT.md`](../manim_utils/README_SCENE_MANAGEMENT.md) - Scene management system
- [`../README.md`](../README.md) - Main project documentation

