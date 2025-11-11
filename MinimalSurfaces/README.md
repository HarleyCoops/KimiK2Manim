# Minimal Surfaces: Mathematical Soap Films in 3D Space

This directory contains a 3D Manim animation project exploring Minimal Surfaces - 
beautiful mathematical surfaces that minimize area, like soap films stretched across wire frames.

## Concept

Minimal surfaces are surfaces with zero mean curvature - they're the mathematical 
equivalent of soap films. When you dip a wire frame into soapy water, the film that 
forms is a minimal surface.

## Key Surfaces

- **Catenoid**: Formed by rotating a catenary curve
- **Helicoid**: A spiral ramp surface
- **Costa Surface**: Complex, intricate minimal surface
- **Enneper Surface**: Self-intersecting minimal surface

## 3D Visualization Emphasis

This project emphasizes:
- **ThreeDScene** rendering (not 2D Scene)
- Dynamic camera movements (orbits, rotations, zooms)
- 3D geometry (surfaces, curves, volumes)
- Artistic presentation with lighting and shadows
- Multiple viewing angles
- Immersive 3D experience

## Files

- `run_pipeline.py` - Pipeline execution script
- `output/` - Generated enriched content (JSON, narrative)

## Running the Pipeline

```bash
cd MinimalSurfaces
python run_pipeline.py
```

This will generate:
- Prerequisite tree exploration
- Mathematical enrichment (equations, definitions)
- 3D visual specifications
- Narrative prompt for Manim ThreeDScene

## Rendering

After pipeline completion, create a Manim scene using `ThreeDScene`:

```python
from manim import *
from manim_utils.managed_scene import ManagedBoundedScene

class MinimalSurfaces3D(ThreeDScene):
    def construct(self):
        # 3D visualization code here
        ...
```

Render with:
```bash
python -m manim -pql minimal_surfaces_scene.py MinimalSurfaces3D
```

