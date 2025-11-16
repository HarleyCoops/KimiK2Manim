# Torus Eigenfunctions Animation

A 3D Manim animation visualizing torus eigenfunctions - the natural standing wave modes of a toroidal surface.

## Overview

This animation cycles through different eigenfunction modes of a torus, showing how the surface's geometry changes with different vibrational patterns. Each mode is indexed by two integers:
- **m**: Number of oscillations around the large circle
- **n**: Number of oscillations around the small circle

Dark regions represent **nodes** (no motion) and bright bands represent **antinodes** (maximum amplitude). As the mode indices increase, nodes crowd together and ridges sharpen, creating increasingly complex patterns.

## Files

- `torus_eigenfunctions.py` - Main animation scene
- `SURFACE_RESEARCH.md` - Research on Manim 3D surface libraries
- `instructions.txt` - Original project requirements
- `Imagereference.jpg` - Reference image for visualization

## Mathematical Background

The eigenfunctions satisfy the eigenvalue equation:
```
Δψ_{m,n} = λ_{m,n} ψ_{m,n}
```

Where:
- `Δ` is the Laplacian operator on the torus surface
- `ψ_{m,n}` is the eigenfunction with mode indices (m, n)
- `λ_{m,n}` is the corresponding eigenvalue (natural frequency)

The eigenfunction used is:
```
ψ_{m,n}(u, v) = cos(m·u) · cos(n·v)
```

This modulates the torus radius, creating the standing wave patterns.

## Animation Timeline (60 seconds)

- **[0-5s]** Introduction and title
- **[5-15s]** Mode (1,1) - Fundamental mode
- **[15-25s]** Mode (2,1) - Two oscillations around large circle
- **[25-35s]** Mode (1,2) - Two oscillations around small circle
- **[35-45s]** Mode (3,2) - Higher frequency mode
- **[45-55s]** Mode (4,3) - Pine-cone appearance
- **[55-60s]** Conclusion

## Rendering

To render the animation:

```bash
# Low quality (fast preview)
python -m manim -pql torus/torus_eigenfunctions.py TorusEigenfunctions

# Medium quality
python -m manim -pqm torus/torus_eigenfunctions.py TorusEigenfunctions

# High quality
python -m manim -pqh torus/torus_eigenfunctions.py TorusEigenfunctions
```

## Surface Modeling

This project uses **Manim's built-in `Surface` class** for 3D surface rendering. See `SURFACE_RESEARCH.md` for details on why this is the optimal choice for Manim animations.

The surface is created using parametric functions:
```python
def torus_eigenfunction(u, v, m, n):
    eigen = amplitude * cos(m * u) * cos(n * v)
    r_modulated = r + eigen
    x = (R + r_modulated * cos(v)) * cos(u)
    y = (R + r_modulated * cos(v)) * sin(u)
    z = r_modulated * sin(v)
    return [x, y, z]
```

## Customization

You can modify the animation by:
- Changing mode sequences in `construct()` method
- Adjusting amplitude in `torus_eigenfunction()` (default: 0.5)
- Modifying colors in `mode_sequence()` calls
- Changing resolution for higher detail (currently adaptive based on mode complexity)

## Requirements

- Manim Community Edition
- NumPy
- Standard Manim dependencies

See main project `requirements.txt` for full dependency list.

